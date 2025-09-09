import streamlit as st

# ========= CONFIGURAÇÃO DO APP =========
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
col1, col2 = st.columns([3, 1])  # proporção 3:1
with col1:
    st.title("BACKOFFICE CBMI")
with col2:
    st.markdown("<h3 style='text-align: right;'>USER: JOÃO RIBAMAR</h3>", unsafe_allow_html=True)

st.subheader("🧮 Cálculo de Custos")

# ========= ENTRADAS =========
pavimento = st.number_input("Digite o tamanho do pavimento (m²)", min_value=0.0, format="%.2f")
paredes = st.number_input("Digite o tamanho das paredes (m²)", min_value=0.0, format="%.2f")

# ========= CÁLCULOS =========
custo_pavimento = pavimento * 9.50
custo_paredes = paredes * 25.00
custo_total = custo_pavimento + custo_paredes

# ========= RESULTADOS =========
st.write(f"💰 Custo do pavimento: **€ {custo_pavimento:.2f}**")
st.write(f"💰 Custo das paredes: **€ {custo_paredes:.2f}**")
st.write(f"✅ Custo total: **€ {custo_total:.2f}**")















