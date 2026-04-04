import streamlit as st
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("📚 " + locale.textos["titulo_ayuda_cargar_ahorro"])
st.write(locale.textos["ayuda_cargar_ahorro_desc_1"])
st.markdown("""---""", unsafe_allow_html=True)

st.write(locale.textos["ayuda_cargar_ahorro_desc_2"])
st.write(locale.textos["ayuda_cargar_ahorro_desc_3"])
st.image("./assets/helps/ahorro_aseguradoras.png")

st.write(locale.textos["ayuda_cargar_ahorro_desc_4"])
st.image("./assets/helps/ahorro_exportar.png")

st.info(locale.textos["ayuda_cargar_ahorro_importante"])
