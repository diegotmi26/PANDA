import streamlit as st
import google_genai as genai # A nova biblioteca que substituiu a generativeai
import os

# Configuração da página
st.set_page_config(page_title="Agente Gemini 3", layout="centered")

# Configuração do Cliente Gemini 3
# A nova SDK utiliza o objeto Client para gerir a ligação
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-3-flash"

st.title("🚀 Interface Oficial Gemini 3")
st.caption("Conexão via Google AI SDK (Atualizado)")

# Inicialização do histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição das mensagens
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Lógica de Chat
if prompt := st.chat_input("Diga algo..."):
    # Adiciona pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada ao modelo Gemini 3 usando a nova sintaxe
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction="Você é um assistente técnico de telecomunicações.",
                temperature=0.7
            )
        )
        
        resposta_texto = response.text
        
        with st.chat_message("assistant"):
            st.markdown(resposta_texto)
        
        st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
        
    except Exception as e:
        st.error(f"Erro na conexão com Gemini 3: {e}")
