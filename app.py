import streamlit as st
from google import genai

# Configuração da Interface
st.set_page_config(page_title="PANDA B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")

# Conexão Segura com a API
try:
    # O app busca a chave nos 'Secrets' que você configurou
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    # Configuração do Modelo (Gemini 3 Flash conforme seu laboratório)
    MODEL_ID = "gemini-3-flash-preview"
    SYS_INSTRUCT = "Você é o PANDA, assistente B2B. Responda apenas com base nos documentos do projeto."

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Como posso ajudar o time de vendas?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Chamada da API 2026
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config={'system_instruction': SYS_INSTRUCT}
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Aguardando configuração: {e}")
