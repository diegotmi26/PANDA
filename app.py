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

    # 5. Resposta do Assistente com Ajuste de Tempo e Retentativa
    with st.chat_message("assistant"):
        placeholder = st.empty()
        
        # Ordem de preferência de modelos (Gemini 3 e 2)
        model_options = ["gemini-2.0-flash", "gemini-2.0-flash-exp"]
        
        success = False
        max_retries = 3  # Tenta até 3 vezes se houver erro de tempo (429)
        retry_delay = 10 # Espera 10 segundos entre as tentativas

        for model_name in model_options:
            if success: break
            
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    
                    output_text = response.text
                    placeholder.markdown(output_text)
                    st.session_state.messages.append({"role": "assistant", "content": output_text})
                    success = True
                    break # Sai do loop de retentativa se der certo
                    
                except Exception as e:
                    error_str = str(e).upper()
                    
                    # AJUSTE DE TEMPO: Se for erro 429, espera e tenta de novo
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        if attempt < max_retries - 1:
                            placeholder.warning(f"⏳ Limite de tempo atingido. Tentando novamente em {retry_delay}s... (Tentativa {attempt + 1}/{max_retries})")
                            time.sleep(retry_delay)
                            placeholder.empty() # Limpa o aviso para a próxima tentativa
                        else:
                            st.error("❌ Limite de requisições excedido. Por favor, aguarde 30 segundos e tente novamente manualmente.")
                            break
                    
                    # Erro 404: Passa para o próximo modelo da lista (gemini-2.0-flash-exp)
                    elif "404" in error_str:
                        break # Sai do loop de retentativa e vai para o próximo modelo
                    
                    else:
                        st.error(f"Erro técnico: {e}")
                        break

        if not success and "404" in error_str:
            st.error("Nenhum modelo compatível foi encontrado. Verifique se o nome do modelo foi descontinuado.")
