import streamlit as st
from google import genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PANDA B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")

# --- CONEXÃO COM A API ---
# Use sua chave AIza...
API_KEY = "COLE_SUA_CHAVE_AQUI" 
client = genai.Client(api_key=API_KEY)

# --- CONFIGURAÇÃO DO MODELO ---
# Em 2026, o nome oficial para a API gratuita é 'gemini-2.0-flash'
MODEL_ID = "gemini-2.0-flash"

# Instrução de Sistema
SYS_INSTRUCT = "Você é o PANDA, assistente de vendas B2B. Responda apenas com base nos documentos do projeto."

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre as ofertas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Nova sintaxe de 2026 para gerar conteúdo
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt,
                config={'system_instruction': SYS_INSTRUCT}
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
            st.info("Dica: Verifique se sua chave de API no AI Studio está ativa para o modelo Gemini 2.0 Flash.")
