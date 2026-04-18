import streamlit as st
import os
from google import genai

# Configuração da Página
st.set_page_config(page_title="A.I.D.A. Gemini 3", layout="centered")

# Inicialização do Cliente
# Use a variável EXATA que você configurou no Secrets do Streamlit
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# ID do modelo para 2026 (Remova o "-preview" se o erro 404 persistir)
MODEL_ID = "gemini-3-flash"

st.title("🤖 Assistente A.I.D.A.")
st.caption("Suporte Técnico Telecom | Motor Gemini 3")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Chamada simplificada - Evita erro de versão de API v1beta
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config={
                "system_instruction": "Você é a A.I.D.A., especialista em telecomunicações.",
                "temperature": 0.7
            }
        )
        
        texto_resposta = response.text
        with st.chat_message("assistant"):
            st.markdown(texto_resposta)
        st.session_state.messages.append({"role": "assistant", "content": texto_resposta})

    except Exception as e:
        st.error(f"Erro na conexão: {e}")
