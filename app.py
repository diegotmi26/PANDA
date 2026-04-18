import streamlit as st
from google import genai

st.set_page_config(page_title="PANDA B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")

# Puxando a chave de forma segura
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Dúvida sobre as regras de Abril/2026?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Usando o modelo que você confirmou no print
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config={'system_instruction': "Você é o PANDA. Use os documentos do projeto."}
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"Erro: {e}")
