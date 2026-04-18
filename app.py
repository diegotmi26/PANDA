import streamlit as st
from google import genai
import time

# 1. Configuração da Página
st.set_page_config(page_title="Assistente Gemini 3", page_icon="🤖")
st.title("🤖 Gemini 3 Flash - Console")
st.caption("Conectado via API Gratuita (Google AI Studio)")

# 2. Configuração de Segurança (Secrets do Streamlit/GitHub)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Erro: Chave de API não encontrada nos Secrets do Streamlit.")
    st.stop()

# 3. Inicialização do Histórico de Mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens salvas no histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Interface de Chat
if prompt := st.chat_input("Como posso ajudar com seus contratos ou automação hoje?"):
    
    # Adiciona e exibe a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Chamada da API com Tratamento de Erro de Quota (Gemini 3)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            # IMPORTANTE: Usando o modelo gemini-3-flash conforme atualizado
            response = client.models.generate_content(
                model="gemini-3-flash", 
                contents=prompt
            )
            
            full_response = response.text
            placeholder.markdown(full_response)
            
            # Salva a resposta do assistente no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            # Tratamento específico para o erro 429 mostrado no seu print
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                error_msg = "⚠️ **Limite atingido:** A cota gratuita do Gemini 3 exige uma pausa. Aguarde 30 segundos antes de enviar a próxima mensagem."
                st.warning(error_msg)
            else:
                st.error(f"Erro inesperado: {str(e)}")
