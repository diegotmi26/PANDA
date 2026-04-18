import streamlit as st
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(page_title="Agente de Vendas IA", page_icon="🤖")

# 2. Configuração da API Key (A Vercel lerá isto das Environment Variables)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("Erro: A variável GOOGLE_API_KEY não foi encontrada. Configure-a na Vercel.")
    st.stop()

genai.configure(api_key=api_key)

# 3. Definição da Personalidade do Agente (System Instruction)
SYSTEM_INSTRUCTION = """
Você é o assistente especializado em consultoria de vendas B2B e backoffice de telecomunicações.
Seu objetivo é apoiar consultores no processamento de contratos e dúvidas técnicas.
Tom de voz: Profissional, assertivo e técnico.
Foco: Regras de telecomunicações, preenchimento de checklists e suporte a vendas.
"""

# 4. Inicialização do Modelo Gemini 3
# Nota: Usamos o gemini-3-flash por ser otimizado e gratuito.
model = genai.GenerativeModel(
    model_name='gemini-3-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# 5. Gestão do Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Interface: Cabeçalho
st.title("🤖 Agente IA - Suporte a Vendas")
st.markdown("Bem-vindo! Este assistente foi configurado para ajudar na validação de processos e dúvidas técnicas.")

# Botão para limpar o chat
if st.sidebar.button("Limpar Histórico"):
    st.session_state.messages = []
    st.rerun()

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Campo de Entrada de Mensagem
if prompt := st.chat_input("Como posso ajudar com o contrato hoje?"):
    # Adicionar mensagem do utilizador ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta com o Gemini 3
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Envia o histórico completo para manter o contexto
            full_prompt = [m["content"] for m in st.session_state.messages]
            response = model.generate_content(prompt)
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Adicionar resposta do assistente ao histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
