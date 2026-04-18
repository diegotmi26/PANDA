import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PANDA - Assistente de Ofertas", page_icon="🐼")

# --- CONFIGURAÇÃO DA API ---
# Substitua pelo seu código que começa com AIza...
API_KEY = "AIzaSyDPEwcdfPkdDIKtUh7XWkw0nK-GvQTC6u0" 

genai.configure(api_key=API_KEY)

# --- CONFIGURAÇÃO DO MODELO ---
# Usando o Flash por ser gratuito e rápido para leitura de arquivos
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Você é o PANDA, um assistente técnico de vendas B2B. Responda perguntas sobre Ofertas e Banda Larga usando apenas os documentos fornecidos. Seja direto e profissional."
)

# --- INTERFACE ---
st.title("🐼 PANDA - Inteligência de Dados")
st.caption("Consultor de Ofertas e Regras de Banda Larga (Abril/2026)")

# Inicializa o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt := st.chat_input("Ex: Posso vender Netflix no B2B?"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta da IA
    with st.chat_message("assistant"):
        try:
            # Busca a resposta no Gemini
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # Adiciona resposta da IA ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erro ao conectar com a IA: {e}")
