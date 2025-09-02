import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO DO APP
# ==============================
st.set_page_config(
    page_title="Tabela de Preços de Demolição",
    page_icon="🏗️",
    layout="wide"
)

# ==============================
# INJEÇÃO DO MANIFEST E ICONES
# ==============================
st.markdown(
    """
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <meta name="theme-color" content="#004aad">
    """,
    unsafe_allow_html=True
)

# ==============================
# INTERFACE PRINCIPAL
# ==============================
st.title("🏗️ Tabela de Preços - Demolição")

# Upload do CSV
uploaded_file = st.file_uploader("📂 Envie o arquivo CSV com a tabela de preços", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Tratamento de dados
    df["Preço (€)"] = pd.to_numeric(df["Preço (€)"], errors="coerce")
    df = df.dropna(subset=["Preço (€)"])

    # ==============================
    # SIDEBAR - FILTROS
    # ==============================
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

    # ==============================
    # TABELA DE SERVIÇOS
    # ==============================
    st.subheader("📋 Lista de Serviços")
    st.dataframe(df_filtrado, use_container_width=True)

    # ==============================
    # DASHBOARD DE ANÁLISE
    # ==============================
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

    # ==============================
    # ÁREA DE EMPOLAMENTO
    # ==============================
    st.subheader("⚙️ Área de Empolamento")

    valor = st.number_input("Digite um valor para empolamento", min_value=0.0, format="%.2f")

    resultado = valor * 0.66
    st.write(f"Resultado (valor × 0,66): **{resultado:.2f}**")

else:
    st.info("👆 Faça upload do arquivo `Tabela_Precos_Demolicao.csv` para visualizar os dados.")
