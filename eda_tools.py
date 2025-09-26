import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para análise exploratória de dados
def eda_dashboard(df):
    st.header("📊 Análise Exploratória de Dados (EDA)")

    # Exibir as 5 primeiras linhas
    st.subheader("👀 Visualização Inicial")
    st.dataframe(df.head())

    # Mostrar dimensões e tipos
    st.subheader("📏 Dimensões e Tipos de Dados")
    st.write(f"**Linhas:** {df.shape[0]} | **Colunas:** {df.shape[1]}")
    st.write("**Tipos de Dados:**")
    st.write(df.dtypes)

    # Estatísticas descritivas
    st.subheader("📈 Estatísticas Descritivas")
    try:
        stats = df.describe(numeric_only=True).round(4)
    except Exception:
        # fallback caso alguma versão do pandas cause erro
        stats = df.describe().round(4)
    st.dataframe(stats)

    # Contagem de valores nulos
    st.subheader("❌ Valores Nulos por Coluna")
    missing = df.isnull().sum()
    st.dataframe(missing[missing > 0])

    # Selecionar coluna para histograma
    st.subheader("📉 Distribuição de Variáveis")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if len(numeric_cols) > 0:
        coluna = st.selectbox("Selecione uma coluna numérica:", numeric_cols)
        if coluna:
            fig, ax = plt.subplots()
            df[coluna].dropna().hist(bins=30, ax=ax)
            ax.set_title(f"Histograma - {coluna}")
            ax.set_xlabel(coluna)
            ax.set_ylabel("Frequência")
            st.pyplot(fig)
    else:
        st.info("Nenhuma coluna numérica disponível para histograma.")

    # Mapa de correlação
    if len(numeric_cols) > 1:
        st.subheader("🔗 Mapa de Correlação")
        fig, ax = plt.subplots(figsize=(6, 4))
        corr = df[numeric_cols].corr()
        cax = ax.matshow(corr, cmap='coolwarm')
        fig.colorbar(cax)
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=90)
        ax.set_yticklabels(numeric_cols)
        st.pyplot(fig)
    else:
        st.info("Não há colunas numéricas suficientes para correlação.")
