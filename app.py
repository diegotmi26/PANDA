import streamlit as st
from google import genai

# 1. Configuração da Interface
st.set_page_config(page_title="Consultoria A.I.D.A.", page_icon="🤖", layout="centered")

st.title("🤖 Assistente de Vendas e Backoffice")
st.caption("Versão Gemini 3 - Alta Performance")
st.markdown("---")

# 2. Conexão Segura com a API (Secrets do Streamlit Cloud)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO: Configure a 'GEMINI_API_KEY' nos Secrets do Streamlit.")
    st.stop()

# Usando cache para não recriar o cliente a cada interação
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# 3. Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Campo de Entrada
if prompt := st.chat_input("Como posso ajudar com os contratos hoje?"):
    
    # Mostrar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Resposta Direta do Assistente
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        try:
            # Chamada direta ao Gemini 3 Flash
            response = client.models.generate_content(
                model="gemini-3-flash", 
                contents=prompt
            )
            
            output_text = response.text
            placeholder.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            error_str = str(e).upper()
            if "429" in error_str:
                st.warning("⚠️ Cota temporária atingida. Aguarde alguns instantes.")
            elif "404" in error_str:
                st.error("❌ Modelo Gemini 3 não encontrado nesta região/chave.")
            else:
                st.error(f"Erro técnico: {e}")
