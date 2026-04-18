import streamlit as st
from google import genai

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="PANDA - B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")
st.markdown("---")

# --- CONEXÃO COM A API ---
# Use a chave que começa com AIza... que você gerou no AI Studio
API_KEY = "AIzaSyDPEwcdfPkdDIKtUh7XWkw0nK-GvQTC6u0" 
client = genai.Client(api_key=API_KEY)

# Configurações do modelo baseado na sua imagem
MODEL_ID = "gemini-3-flash-preview"
SYS_INSTRUCT = "Você é o PANDA. Use os documentos do projeto para responder sobre Ofertas B2B da Vivo."

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Dúvida sobre regras de Banda Larga?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Comando oficial da biblioteca google-genai em 2026
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config={'system_instruction': SYS_INSTRUCT}
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Erro na conexão com o PANDA: {e}")
