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
import streamlit as st
import pytesseract
from PIL import Image
import re
import io

# Se for trabalhar com PDF
from pdf2image import convert_from_bytes

st.title("📐 Leitor de Plantas (Simplificado)")

uploaded_file = st.file_uploader("Envie a planta em PDF ou imagem", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    # Se for PDF → converte para imagem
    if uploaded_file.type == "application/pdf":
        pages = convert_from_bytes(uploaded_file.read())
        image = pages[0]  # pega só a primeira página
    else:
        image = Image.open(uploaded_file)

    st.image(image, caption="Planta enviada", use_column_width=True)

    # OCR para extrair texto
    text = pytesseract.image_to_string(image, lang="por")

    # Procura áreas em m² (ex: "12 m²", "20.5m²")
    matches = re.findall(r"(\d+(?:[\.,]\d+)?)\s*m²", text, re.IGNORECASE)

    if matches:
        # Converte para float
        areas = [float(a.replace(",", ".")) for a in matches]
        total_area = sum(areas)

        st.subheader("📊 Resultado")
        st.write("Áreas encontradas:", areas)
        st.write(f"**Área total estimada:** {total_area:.2f} m²")
    else:
        st.warning("⚠️ Nenhuma área em m² foi encontrada no texto da planta.")

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









