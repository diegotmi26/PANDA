import streamlit as st
from google import genai
import time

# 1. Configuração da Interface
st.set_page_config(page_title="Consultoria A.I.D.A.", page_icon="🤖", layout="centered")

st.title("🤖 Assistente de Vendas e Backoffice")
st.markdown("---")

# 2. Conexão Segura com a API (Secrets)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("ERRO: Configure a 'GEMINI_API_KEY' nos Secrets do Streamlit Cloud.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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

    # 5. Resposta do Assistente com Tratamento de Erros (404 e 429)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        # Lista de modelos por ordem de preferência para evitar o erro 404
        # O modelo 'gemini-2.0-flash' é o mais estável para a v1beta atualmente
        model_options = ["gemini-2.0-flash", "gemini-2.0-flash-exp"]
        
        success = False
        for model_name in model_options:
            if success: break
            
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                output_text = response.text
                placeholder.markdown(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
                success = True
                
            except Exception as e:
                error_str = str(e).upper()
                
                # Tratamento do Erro 429 (Quota Exceeded) do seu print
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    st.warning("⚠️ Limite de uso atingido. Aguarde 30 segundos para a próxima pergunta.")
                    time.sleep(2)
                    break 
                
                # Tratamento do Erro 404 (Not Found) - Tenta o próximo modelo da lista
                elif "404" in error_str:
                    continue
                
                else:
                    st.error(f"Erro técnico: {e}")
                    break

        if not success and "404" in error_str:
            st.error("Nenhum modelo compatível foi encontrado na sua região de API.")
