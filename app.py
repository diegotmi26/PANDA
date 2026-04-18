import streamlit as st
import google.gemini as gemini

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PANDA B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")

# --- CONEXÃO COM A API ATUALIZADA ---
API_KEY = "SUA_CHAVE_AQUI"
client = gemini.Client(api_key=API_KEY)

# --- CONFIGURAÇÃO DO ASSISTENTE ---
# Em 2026, usamos o modelo gemini-2.0-flash para velocidade e gratuidade
model_id = "gemini-2.0-flash"

# Instrução de Sistema
sys_instruct = "Você é o PANDA. Use os documentos do projeto para responder sobre Ofertas B2B."

# --- INTERFACE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Dúvida sobre Banda Larga?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Nova forma de gerar conteúdo em 2026
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=gemini.types.GenerateContentConfig(
                    system_instruction=sys_instruct,
                    temperature=0.2
                )
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro na API Gemini 2026: {e}")
