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

st.title("📋 CBMI - Assistente Simples de Perguntas")

uploaded_file = st.file_uploader("📁 Envie um arquivo PDF, Excel ou CSV", type=["pdf", "xlsx", "xls", "csv"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_table(file, ext):
    if ext == "csv":
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    # Concatenar todas as células em uma lista de frases
    textos = []
    for col in df.columns:
        textos.extend(df[col].astype(str).tolist())
    return textos

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    if ext == "pdf":
        text = extract_text_from_pdf(uploaded_file)
        # Quebrar em frases simples por linhas
        frases = [linha.strip() for linha in text.split('\n') if linha.strip()]
    elif ext in ["xlsx", "xls", "csv"]:
        frases = extract_text_from_table(uploaded_file, ext)
    else:
        st.error("Arquivo não suportado")
        st.stop()

    pergunta = st.text_input("❓ Faça sua pergunta:")

    if pergunta:
        # Busca as 5 frases mais similares à pergunta
        resultados = process.extract(pergunta, frases, limit=5)
        st.subheader("💡 Possíveis respostas encontradas:")
        for frase, score in resultados:
            st.write(f"**{score}%** similar: {frase}")


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



