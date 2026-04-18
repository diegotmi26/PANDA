import streamlit as st
import os
# Usando a importação direta para garantir compatibilidade
from google import genai
from google.genai import types

# Configuração da Página
st.set_page_config(page_title="A.I.D.A. Gemini 3", layout="centered")

# Inicialização do Cliente
# Certifique-se de que a variável GOOGLE_API_KEY está nos Secrets do Streamlit
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# Nome do modelo corrigido para a versão estável
MODEL_ID = "gemini-3-flash"

st.title("🤖 Assistente A.I.D.A.")
st.caption("Conexão Estável com Gemini 3 Flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Chamada simplificada para evitar erro de versão de API
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="Você é a A.I.D.A., assistente de telecomunicações.",
                temperature=0.7
            )
        )
        
        resposta = response.text
        with st.chat_message("assistant"):
            st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})

    except Exception as e:
        # Se o erro 404 persistir, o código abaixo ajudará a identificar o nome correto do modelo no seu projeto
        st.error(f"Erro: {e}")
