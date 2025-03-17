import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Chat Interface", layout="wide")

API_BASE_URL = "http://localhost:8080/coder-buddy/v1"


# Inicializar session_state para controle do scroll
def initialize_session():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "scroll_trigger" not in st.session_state:
        st.session_state["scroll_trigger"] = False


initialize_session()


# Função para obter todos os chats
def get_all_chats():
    try:
        response = requests.get(f"{API_BASE_URL}/chats")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar chats: {e}")
        return []


# Função para enviar uma mensagem
def send_message(chat_id, message, tools):
    payload = {
        "message": {"role": "user", "content": message},
        "tools": tools if tools else [],
    }
    try:
        response = requests.post(f"{API_BASE_URL}/chat/{chat_id}/message", json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get("response", None)
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar mensagem: {e}")
        return None


# Sidebar para exibir os chats
st.sidebar.title("Chats")
chats = get_all_chats()
if chats:
    chat_ids = [chat["id"] for chat in chats]
    chat_names = {chat["id"]: chat["name"] for chat in chats}
    selected_chat = st.sidebar.selectbox(
        "Selecione um chat",
        chat_ids,
        format_func=lambda x: chat_names.get(x, "Chat desconhecido"),
    )
else:
    selected_chat = None

# Área principal para exibir o histórico do chat e enviar mensagens
if selected_chat:
    st.title(f"Chat: {chat_names.get(selected_chat, 'Chat desconhecido')}")

    # Buscar histórico do chat
    chat_history = next((chat for chat in chats if chat["id"] == selected_chat), None)
    chat_container = st.empty()

    # Exibir mensagens de forma dinâmica
    with chat_container.container():
        if chat_history and "conversations" in chat_history:
            st.session_state["messages"] = []  # Resetar histórico
            for conversation in chat_history["conversations"]:
                st.session_state["messages"].append(
                    f"**Usuário:** {conversation['question']['message']['content']}"
                )
                if conversation.get("answer"):
                    st.session_state["messages"].append(
                        f"**Assistente:** {conversation['answer']['message']['content']}"
                    )

            for message in st.session_state["messages"]:
                st.write(message)

    # Acionar scroll automático na primeira renderização e após envio de mensagem
    if not st.session_state["scroll_trigger"] or "new_message_sent" in st.session_state:
        st.markdown(
            """
            <script>
            function scrollToBottom() {
                var chatBox = window.parent.document.querySelector("section.main");
                if (chatBox) {
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            }
            setTimeout(scrollToBottom, 500);
            </script>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["scroll_trigger"] = True

    # Campo de entrada para enviar uma nova mensagem
    new_message = st.text_area("Digite sua mensagem")
    tool_type = st.text_input("Tipo de ferramenta (ex: file_search)")
    tool_index = st.text_input("Índice da ferramenta (separado por vírgula)")

    if st.button("Enviar"):
        if new_message.strip():
            tools = []
            if tool_type and tool_index:
                tools.append({"type": tool_type, "index": tool_index.split(",")})

            response = send_message(selected_chat, new_message, tools)
            if response:
                st.session_state["messages"].append(f"**Usuário:** {new_message}")
                st.session_state["messages"].append(f"**Assistente:** {response}")
                st.session_state["scroll_trigger"] = False  # Força novo scroll
                st.session_state["new_message_sent"] = True  # Marca atualização
                st.rerun()  # Força atualização da tela
            else:
                st.error("Erro ao processar a resposta do servidor.")
        else:
            st.warning("A mensagem não pode estar vazia.")
