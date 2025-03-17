import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Chat Interface", layout="wide")

API_BASE_URL = "http://localhost:8080/coder-buddy/v1"

# Inicializar session_state para controle do scroll e mensagens
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

# Função para criar um novo chat
def create_chat(chat_name, tools):
    payload = {"name": chat_name, "config": {"tools": tools}}
    try:
        response = requests.post(f"{API_BASE_URL}/chat", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao criar chat: {e}")
        return None

# Função para enviar uma mensagem
def send_message(chat_id, message, tools):
    payload = {"message": {"role": "user", "content": message}, "tools": tools if tools else []}
    try:
        response = requests.post(f"{API_BASE_URL}/chat/{chat_id}/message", json=payload)
        response.raise_for_status()
        return response.json().get("response", "Nenhuma resposta recebida.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar mensagem: {e}")
        return None

# Sidebar para exibir e criar chats
st.sidebar.title("Chats")

chats = get_all_chats()
chat_ids = [chat["id"] for chat in chats]
chat_names = {chat["id"]: chat["name"] for chat in chats}

selected_chat = None
if chat_ids:
    selected_chat = st.sidebar.selectbox(
        "Selecione um chat",
        chat_ids,
        format_func=lambda x: chat_names.get(x, "Chat desconhecido"),
    )

# Criar novo chat
st.sidebar.subheader("Criar Novo Chat")
new_chat_name = st.sidebar.text_input("Nome do chat", key="new_chat_name")
tool_type = st.sidebar.text_input("Ferramenta (ex: file_search)", key="tool_type")
tool_index = st.sidebar.text_input("Índice da ferramenta (separado por vírgula)", key="tool_index")

if st.sidebar.button("Criar Chat"):
    tools = []
    if tool_type and tool_index:
        tools.append({"type": tool_type, "index": tool_index.split(",")})

    new_chat = create_chat(new_chat_name, tools)
    if new_chat:
        st.success("Chat criado com sucesso! Selecione na lista.")
        st.rerun()

# Área principal para exibir histórico do chat e enviar mensagens
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
                question = conversation.get("question", {})
                answer = conversation.get("answer", {})

                user_message = question.get("message", {}).get("content", "Mensagem não encontrada")
                assistant_message = answer.get("message", {}).get("content", "Sem resposta")

                st.session_state["messages"].append(f"**Usuário:** {user_message}")
                if assistant_message != "Sem resposta":
                    st.session_state["messages"].append(f"**Assistente:** {assistant_message}")

            for message in st.session_state["messages"]:
                st.write(message)

    # Campo de entrada para enviar uma nova mensagem
    new_message = st.text_area("Digite sua mensagem", key="new_message")
    tool_type_input = st.text_input("Tipo de ferramenta (ex: file_search)", key="tool_type_input")
    tool_index_input = st.text_input("Índice da ferramenta (separado por vírgula)", key="tool_index_input")

    if st.button("Enviar"):
        if new_message.strip():
            tools = []
            if tool_type_input and tool_index_input:
                tools.append({"type": tool_type_input, "index": tool_index_input.split(",")})

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