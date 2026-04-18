import streamlit as st
import google.generativeai as genai
import os

# 1. Configuração de Segurança e API
# No Gemini 3, a biblioteca deve estar na versão 0.8.0 ou superior
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 2. Seleção do Modelo Atualizado
# ATENÇÃO: Substituímos o 1.5 pelo 'gemini-3-flash'
MODEL_ID = 'gemini-3-flash'

# 3. Configuração do Agente (System Instruction)
# Aqui é onde você define a "alma" do seu assistente
instruction = "Você é um especialista em backoffice de telecomunicações para o mercado brasileiro."

model = genai.GenerativeModel(
    model_name=MODEL_ID,
    system_instruction=instruction
)

# 4. Interface Streamlit
st.set_page_config(page_title="Agente Telecom Gemini 3")
st.title("Conexão Gemini 3 - Google AI Studio")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Exibição de mensagens
for content in st.session_state.chat.history:
    role = "assistant" if content.role == "model" else "user"
    with st.chat_message(role):
        st.markdown(content.parts[0].text)

# Entrada de novas perguntas
if prompt := st.chat_input("Como posso ajudar?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = st.session_state.chat.send_message(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
