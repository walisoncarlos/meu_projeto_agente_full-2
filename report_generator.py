import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd
import io
from datetime import datetime

def gerar_relatorio(df: pd.DataFrame, nome_relatorio="relatorio_eda.pdf") -> io.BytesIO:
    """Gera um relatório PDF com informações e estatísticas do DataFrame.
    Retorna o arquivo PDF como BytesIO para download no Streamlit.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []
    estilos = getSampleStyleSheet()

    # Cabeçalho
    titulo = Paragraph("Agentes Autônomos - Relatório de Análise de Dados", estilos["Title"])
    data_geracao = Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilos["Normal"])
    elementos.extend([titulo, Spacer(1, 12), data_geracao, Spacer(1, 20)])

    # Informações básicas
    elementos.append(Paragraph("📋 Informações Básicas", estilos["Heading2"]))
    info = f"Linhas: {df.shape[0]} - Colunas: {df.shape[1]}"
    elementos.append(Paragraph(info, estilos["Normal"]))
    elementos.append(Spacer(1, 12))

    # Estatísticas descritivas (limit numeric)
    elementos.append(Paragraph("📈 Estatísticas Descritivas", estilos["Heading2"]))
    stats = df.describe(numeric_only=True).fillna(0).round(4)
    # build a small table for stats (transpose for readability)
    stats_t = stats.T.reset_index()
    data = [list(stats_t.columns)] + stats_t.values.tolist()
    tabela_stats = Table(data, hAlign='LEFT')
    tabela_stats.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    elementos.append(tabela_stats)
    elementos.append(Spacer(1, 12))

    # Valores nulos
    elementos.append(Paragraph("⚠️ Valores Nulos", estilos["Heading2"]))
    nulos = df.isnull().sum()
    tabela_nulos = Table([["Coluna", "Nulos"]] + [[col, int(nulos[col])] for col in nulos.index], hAlign='LEFT')
    tabela_nulos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    elementos.append(tabela_nulos)
    elementos.append(PageBreak())

    # Finalizar PDF
    doc.build(elementos)
    buffer.seek(0)
    return buffer
