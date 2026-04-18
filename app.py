import streamlit as st
from google import genai
from google.genai import types
import os

# Configuração da Interface
st.set_page_config(page_title="A.I.D.A. - Gemini 3 Flash", layout="wide")

# Inicialização do Cliente com a nova SDK
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# Configurações do Agente
MODEL_NAME = "gemini-3-flash"
SYSTEM_INSTRUCTION = """
Você é a A.I.D.A., assistente de elite em backoffice e vendas de telecomunicações.
Seu foco é suporte técnico, conferência de contratos e auxílio a consultores.
Respostas rápidas, precisas e profissionais.
"""

st.title("🤖 A.I.D.A. | Inteligência de Dados e Apoio")
st.info("Operando com motor Gemini 3 Flash (Versão 2026)")

# Histórico de Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Exibição do Chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de Usuário
if prompt := st.chat_input("Como posso ajudar no seu processo de venda?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Geração de Resposta com Gemini 3 Flash
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2, # Menor temperatura para maior precisão técnica
            )
        )
        
        answer = response.text
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error(f"Erro na conexão com Gemini 3 Flash: {e}")
