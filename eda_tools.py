import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- Função para carregar dados ---
def carregar_dados(arquivo):
    """Carrega um arquivo CSV e retorna um DataFrame."""
    try:
        df = pd.read_csv(arquivo)
        st.success("✅ Arquivo carregado com sucesso!")
        return df
    except Exception as e:
        st.error(f"❌ Erro ao carregar o arquivo: {e}")
        return None

# --- Mostrar informações básicas ---
def info_basica(df):
    """Mostra informações básicas do DataFrame."""
    st.subheader("📊 Informações Básicas")
    st.write(f"**Número de Linhas:** {df.shape[0]}")
    st.write(f"**Número de Colunas:** {df.shape[1]}")
    st.write("**Colunas:**", list(df.columns))
    st.write("**Tipos de Dados:**")
    st.dataframe(df.dtypes.astype(str))

# --- Estatísticas descritivas ---
def estatisticas(df):
    """Exibe estatísticas descritivas do DataFrame."""
    st.subheader("📈 Estatísticas Descritivas")
    try:
        st.dataframe(df.describe(numeric_only=True).round(4))
    except Exception as e:
        st.error(f"Erro ao calcular estatísticas: {e}")

# --- Mostrar valores nulos ---
def valores_nulos(df):
    """Mostra a quantidade de valores nulos por coluna."""
    st.subheader("⚠️ Valores Nulos")
    st.dataframe(df.isnull().sum())

# --- Gráfico de histograma ---
def histograma(df, coluna):
    """Gera um histograma de uma coluna numérica."""
    st.subheader(f"📊 Histograma - {coluna}")
    fig, ax = plt.subplots()
    try:
        series = pd.to_numeric(df[coluna], errors='coerce').dropna()
        series.hist(ax=ax, bins=30)
        ax.set_xlabel(coluna)
        ax.set_ylabel('Frequência')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao gerar histograma: {e}")

# --- Mapa de correlação ---
def mapa_correlacao(df):
    """Gera um mapa de correlação entre variáveis numéricas."""
    st.subheader("🔗 Mapa de Correlação")
    try:
        corr = df.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(8,6))
        cax = ax.matshow(corr, cmap=plt.cm.coolwarm)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        fig.colorbar(cax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao gerar mapa de correlação: {e}")
