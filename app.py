import streamlit as st
import pandas as pd
from pathlib import Path

# ========= CONFIGURAÇÃO DO APP =========
static_dir = Path(__file__).parent

st.set_page_config(
    page_title="CBMI APP",
    page_icon="apple-touch-icon.png",  # Ícone no navegador
    layout="wide"
)

# Força Safari/iOS a usar o ícone certo
st.markdown(
    """
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    <link rel="icon" href="apple-touch-icon.png">
    """,
    unsafe_allow_html=True
)

# ========= CABEÇALHO =========
st.title("🏗️ CBMI - Tabela de Preços de Demolição")
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from fuzzywuzzy import process
import zipfile
import io
import os
from PIL import Image

st.title("📦 CBMI - Perguntas com Arquivos ZIP (com origem da resposta)")

uploaded_file = st.file_uploader("📁 Envie um ZIP com arquivos PDF, Excel ou CSV", type=["zip"])

# Funções auxiliares

def extract_text_from_pdf(file_stream):
    text = ""
    with fitz.open(stream=file_stream, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_table(file_stream, ext):
    if ext == "csv":
        df = pd.read_csv(file_stream)
    else:
        df = pd.read_excel(file_stream)
    textos = []
    for idx, row in df.iterrows():
        linha_texto = " | ".join(row.astype(str))
        textos.append((linha_texto, idx, df))  # Guardar índice e dataframe
    return textos

def process_file(filename, file_stream):
    ext = filename.split(".")[-1].lower()
    if ext == "pdf":
        text = extract_text_from_pdf(file_stream)
        frases = [linha.strip() for linha in text.split('\n') if linha.strip()]
        return [{"arquivo": filename, "texto": f, "preview": None} for f in frases]
    elif ext in ["xlsx", "xls", "csv"]:
        linhas = extract_text_from_table(file_stream, ext)
        return [{"arquivo": filename, "texto": linha, "preview": df.iloc[[idx]]} for linha, idx, df in linhas]
    else:
        return []

# === Processamento do ZIP ===

frases_total = []

if uploaded_file:
    with zipfile.ZipFile(uploaded_file) as z:
        for name in z.namelist():
            if name.endswith(('.pdf', '.xlsx', '.xls', '.csv')):
                st.info(f"📄 Processando arquivo: {name}")
                with z.open(name) as f:
                    file_bytes = io.BytesIO(f.read())
                    frases = process_file(name, file_bytes)
                    frases_total.extend(frases)

# === Interface de pergunta ===

if frases_total:
    pergunta = st.text_input("❓ Faça sua pergunta com base no conteúdo dos arquivos:")
    if pergunta:
        # Coletar todos os textos para comparação
        corpus = [f["texto"] for f in frases_total]
        resultados = process.extract(pergunta, corpus, limit=5)

        st.subheader("💡 Resultados mais parecidos com sua pergunta:")

        for match_texto, score in resultados:
            # Encontrar a entrada original que contém esse texto
            entrada = next((f for f in frases_total if f["texto"] == match_texto), None)
            if not entrada:
                continue

            st.markdown(f"""
            **🎯 Similaridade:** {score}%  
            **📁 Arquivo:** `{entrada['arquivo']}`  
            **📝 Trecho:** {match_texto}
            """)

            # Mostrar prévia se for Excel/CSV
            if entrada["preview"] is not None:
                st.write("📊 Linha correspondente:")
                st.dataframe(entrada["preview"])


# ========= UPLOAD DO CSV =========
uploaded_file = st.file_uploader("📂 Envie o arquivo CSV com a tabela de preços", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Garantir que preços são numéricos
    df["Preço (€)"] = pd.to_numeric(df["Preço (€)"], errors="coerce")
    df = df.dropna(subset=["Preço (€)"])

    # ========= SIDEBAR - FILTROS =========
    st.sidebar.header("🔍 Filtros")
    categoria = st.sidebar.selectbox("Escolha uma categoria", ["Todas"] + df["Categoria"].unique().tolist())

    if categoria != "Todas":
        df_filtrado = df[df["Categoria"] == categoria]
    else:
        df_filtrado = df

    # Campo de pesquisa
    st.sidebar.header("🔎 Pesquisa")
    pesquisa = st.sidebar.text_input("Digite parte do nome do serviço ou categoria")

    if pesquisa:
        df_filtrado = df_filtrado[
            df_filtrado["Serviço"].str.contains(pesquisa, case=False, na=False) |
            df_filtrado["Categoria"].str.contains(pesquisa, case=False, na=False)
        ]

    # ========= TABELA =========
    st.subheader("📋 Lista de Serviços")
    st.dataframe(df_filtrado, use_container_width=True)

    # ========= DASHBOARD =========
    st.subheader("📊 Dashboard de Análise")
    col1, col2 = st.columns(2)

    with col1:
        if not df_filtrado.empty:
            preco_medio = df_filtrado.groupby("Categoria")["Preço (€)"].mean()
            st.write("Preço médio por categoria (€)")
            st.bar_chart(preco_medio)
        else:
            st.warning("Nenhum dado encontrado para exibir o gráfico.")

    with col2:
        if not df_filtrado.empty:
            qtd_servicos = df_filtrado["Categoria"].value_counts()
            st.write("Quantidade de serviços por categoria")
            st.bar_chart(qtd_servicos)
        else:
            st.warning("Nenhum dado encontrado para exibir o gráfico.")

    # ========= ÁREA DE EMPOLAMENTO =========
    st.subheader("⚙️ Área de Empolamento")
    valor = st.number_input("Digite um valor para empolamento", min_value=0.0, format="%.2f")
    resultado = valor * 0.66
    st.write(f"Resultado (valor × 0,66): **{resultado:.2f}**")

else:
    st.info("👆 Faça upload do arquivo `Tabela_Precos_Demolicao.csv` para visualizar os dados.")





