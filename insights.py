import streamlit as st
import google.generativeai as genai
import pandas as pd

def gerar_conclusoes(df: pd.DataFrame) -> str:
    """Gera conclusões e insights usando Gemini a partir de um DataFrame."""
    GOOGLE_API_KEY = st.secrets["general"]["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Prepare a succinct description to send to the model (avoid huge dumps)
    desc = df.describe(numeric_only=True).round(4).to_string()
    missing = df.isnull().sum().to_string()
    top5 = df.head(5).to_string()

    prompt = f"""Você é um assistente especialista em análise de dados.
    Com base nas estatísticas abaixo, gere até 6 conclusões claras (curtas) sobre os dados.
    Indique padrões, variáveis possivelmente correlacionadas, presença de outliers e sugestões de próximos passos.
    Estatísticas:
    {desc}

    Valores nulos por coluna:
    {missing}

    Amostra (5 primeiras linhas):
    {top5}
    """

    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)
