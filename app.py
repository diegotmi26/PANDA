import streamlit as st
from google import genai

# 1. Configuração da Interface
st.set_page_config(page_title="Consultoria A.I.D.A.", page_icon="🤖", layout="centered")

st.title("🤖 Assistente de Vendas e Backoffice")
st.caption("Conectado via Gemini 2.0 Flash (Alta Velocidade)")
st.markdown("---")

# 2. Conexão Segura com a API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO: Configure a 'GEMINI_API_KEY' nos Secrets do Streamlit Cloud.")
    st.stop()

# Cache do cliente para evitar processos duplicados
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# 3. Inicialização do Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Entrada do Usuário
if prompt := st.chat_input("Como posso ajudar hoje?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Resposta Instantânea
    with st.chat_message("assistant"):
        try:
            # Usando gemini-2.0-flash para evitar o erro 404 de "não encontrado"
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            output_text = response.text
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            error_msg = str(e).upper()
            if "429" in error_msg:
                st.error("⚠️ Limite de cota atingido. Como a conta é nova, aguarde 1 minuto.")
            elif "404" in error_msg:
                st.error("❌ Modelo não disponível. Tente trocar para 'gemini-1.5-flash' no código.")
            else:
                st.error(f"Erro inesperado: {e}")
