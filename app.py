import streamlit as st
from google import genai

# Configuração da página
st.set_page_config(page_title="Assistente Gemini", layout="centered")
st.title("🤖 Meu Chatbot Gemini")

# Recupera a chave dos segredos do Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

# Inicializa o histórico do chat se não existir
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Como posso ajudar?"):
    # Adiciona pergunta do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta usando o modelo gratuito (ex: gemini-2.0-flash ou gemini-3-flash-preview)
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # Ou o modelo gratuito disponível no momento
                    contents=prompt
                )
                full_response = response.text
                st.markdown(full_response)
                
                # Salva a resposta no histórico
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Erro na API: {e}")
