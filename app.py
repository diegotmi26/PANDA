import streamlit as st
from google import genai  # Nova SDK oficial pós-descontinuação
from google.genai import types
import os

# 1. Configuração da Interface
st.set_page_config(page_title="Agente A.I.D.A. - Gemini 3", page_icon="🤖")

# 2. Configuração do Cliente Gemini 3
# A nova SDK exige a criação de um cliente central
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Chave de API não configurada nas variáveis de ambiente.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3-flash"  # Versão recomendada para 2026

# 3. Definição da Personalidade (System Instruction)
SYSTEM_PROMPT = """
Você é a A.I.D.A. (Ampla Inteligência de Dados e Apoio).
Especialista em backoffice e suporte a consultores de vendas de telecomunicações.
Seu tom é técnico, prestativo e focado em resolver pendências contratuais.
"""

# 4. Gestão do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título da aplicação
st.title("🤖 Assistente A.I.D.A.")
st.subheader("Suporte em Telecomunicações - Gemini 3")

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de Chat
if prompt := st.chat_input("Como posso ajudar com a venda de hoje?"):
    # Adicionar pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada ao modelo usando a sintaxe atualizada do Gemini 3
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            ),
        )
        
        full_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Erro na API do Gemini 3: {e}")
