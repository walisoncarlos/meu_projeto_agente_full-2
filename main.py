import streamlit as st
import agent
import eda_tools as eda
import report_generator as rg
import pandas as pd

st.set_page_config(page_title="Agente Autônomo - Dashboard", page_icon="🤖", layout="wide")

# --- Título ---
st.title("🤖 Painel Principal - Agente Autônomo com Gemini & EDA")

# --- Menu ---
menu = st.sidebar.selectbox(
    "📂 Escolha a funcionalidade:",
    ["🏠 Início", "💬 Agente Gemini", "📊 Análise Exploratória de Dados"]
)

# --- Página Início ---
if menu == "🏠 Início":
    st.markdown("""
    ### 👋 Bem-vindo ao Agente Autônomo
    Este aplicativo combina **IA Conversacional (Gemini)** com **Ferramentas de EDA**.

    Use o menu lateral para navegar:
    - 💬 **Agente Gemini**: Converse com o modelo de linguagem.
    - 📊 **EDA**: Faça análise exploratória de dados CSV.
    """)

# --- Página Agente Gemini ---
elif menu == "💬 Agente Gemini":
    st.header("💬 Chat com o Modelo Gemini")
    agent.run()

# --- Página de EDA ---
elif menu == "📊 Análise Exploratória de Dados":
    st.header("📊 Ferramenta de EDA")
    arquivo = st.file_uploader("📁 Envie um arquivo CSV", type=["csv"])

    if arquivo is not None:
        df = eda.carregar_dados(arquivo)
        if df is not None:
            eda.info_basica(df)
            eda.estatisticas(df)
            eda.valores_nulos(df)
            colunas_numericas = df.select_dtypes(include='number').columns
            if len(colunas_numericas) > 0:
                coluna = st.selectbox("Selecione uma coluna para o histograma:", colunas_numericas)
                eda.histograma(df, coluna)
                eda.mapa_correlacao(df)

            # Insights (com IA)
            if st.button("🧠 Gerar Conclusões Automáticas com Gemini"):
                try:
                    from insights import gerar_conclusoes
                    with st.spinner("Analisando com IA..."):
                        conclusoes = gerar_conclusoes(df)
                        st.markdown("### 🧠 Conclusões da Análise")
                        st.write(conclusoes)
                except Exception as e:
                    st.error(f"Erro ao gerar conclusões: {e}")

            # Gerar PDF de relatório
            if st.button("📄 Gerar Relatório PDF"):
                try:
                    buffer = rg.gerar_relatorio(df)
                    st.success("✅ Relatório gerado com sucesso!")
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=buffer.getvalue() if hasattr(buffer, 'getvalue') else buffer,
                        file_name="relatorio_eda.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
