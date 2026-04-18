import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PANDA - Assistente B2B", page_icon="🐼")
st.title("🐼 PANDA - Inteligência de Dados")

# --- CONFIGURAÇÃO DA API ---
# Use a sua chave que termina em ...E8fQ
API_KEY = "COLE_SUA_CHAVE_AQUI" 

genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÃO DO MODELO ATUALIZADO (2026) ---
# Mudamos de 'gemini-1.5-flash' para 'gemini-2.0-flash'
try:
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        system_instruction="Você é o PANDA, assistente de vendas B2B. Responda perguntas sobre Ofertas e Banda Larga usando os documentos fornecidos."
    )
except:
    # Caso o 2.0 ainda esteja em rollout na sua região, tentamos o nome genérico
    model = genai.GenerativeModel(model_name='gemini-flash')

# --- HISTÓRICO E CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pergunte algo sobre as ofertas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro na resposta: {e}")
