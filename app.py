import streamlit as st
import os
from google import genai
from google.genai import types

# 1. Conexão com a Chave do Studio
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("A.I.D.A. com Google Search")

if prompt := st.chat_input("Pesquise regras de Telecom..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Configurações que você trouxe do código do Studio
    config = types.GenerateContentConfig(
        temperature=0.3,
        tools=[types.Tool(googleSearch=types.GoogleSearch())], # Habilita o Google no seu App
        thinking_config=types.ThinkingConfig(thinking_level="HIGH") # Faz a IA pensar antes de responder
    )

    # 3. Gerando a resposta com Stream (aparecendo aos poucos)
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-3-flash",
            contents=prompt,
            config=config
        )
        st.markdown(response.text)
