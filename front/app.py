import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Chat Interface", layout="wide")

API_BASE_URL = "http://localhost:8080/coder-buddy/v1"

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
        "tools": tools if tools else []
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
    selected_chat = st.sidebar.selectbox("Selecione um chat", chat_ids, format_func=lambda x: chat_names.get(x, "Chat desconhecido"))
else:
    selected_chat = None

# Área principal para exibir o histórico do chat e enviar mensagens
if selected_chat:
    st.title(f"Chat: {chat_names.get(selected_chat, 'Chat desconhecido')}")
    
    # Buscar histórico do chat
    chat_history = next((chat for chat in chats if chat["id"] == selected_chat), None)
    if chat_history and "conversations" in chat_history:
        for conversation in chat_history["conversations"]:
            st.write(f"**Usuário:** {conversation['question']['message']['content']}")
            if conversation.get("answer"):
                st.write(f"**Assistente:** {conversation['answer']['message']['content']}")
    
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
                # Verifica se a resposta contém código e formata corretamente
                if "```" in response:
                    st.markdown(response)
                else:
                    try:
                        formatted_response = json.loads(response)
                        st.json(formatted_response)
                    except json.JSONDecodeError:
                        st.write(response)
            else:
                st.error("Erro ao processar a resposta do servidor.")
        else:
            st.warning("A mensagem não pode estar vazia.")