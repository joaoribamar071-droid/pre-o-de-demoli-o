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
import fitz  # PyMuPDF

st.subheader("🔍 Buscar palavras-chave em arquivos")
st.write("Envie um arquivo PDF, Excel ou CSV e veja se ele contém as palavras que você está procurando.")

uploaded_file = st.file_uploader("📁 Enviar arquivo", type=["pdf", "xlsx", "xls", "csv"], key="file_upload_busca")

keywords_input = st.text_input("🔑 Palavras-chave (separadas por vírgula)", key="keyword_input")

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
    return df

if uploaded_file and keywords_input:
    ext = uploaded_file.name.split(".")[-1].lower()
    keywords = [k.strip().lower() for k in keywords_input.split(",")]

    st.subheader("🔎 Resultados")

    if ext == "pdf":
        text = extract_text_from_pdf(uploaded_file).lower()
        for keyword in keywords:
            if keyword in text:
                st.success(f"✅ Palavra-chave **{keyword}** encontrada.")
            else:
                st.warning(f"⚠️ Palavra-chave **{keyword}** NÃO encontrada.")

    elif ext in ["xlsx", "xls", "csv"]:
        df = extract_text_from_table(uploaded_file, ext)
        found_any = False
        content = df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep=' ').lower()

        for keyword in keywords:
            if keyword in content:
                st.success(f"✅ Palavra-chave **{keyword}** encontrada.")
                found_any = True
            else:
                st.warning(f"⚠️ Palavra-chave **{keyword}** NÃO encontrada.")

        if found_any:
            st.dataframe(df)

    else:
        st.error("❌ Tipo de arquivo não suportado.")

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

