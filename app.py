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
st.title("BACKOFFICE CBMI")

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













