import streamlit as st
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("📚 " + locale.textos["titulo_ayuda_cargar_caja"])
st.write(locale.textos["ayuda_cargar_caja_desc_1"])
st.markdown("""---""", unsafe_allow_html=True)

st.write(locale.textos["ayuda_cargar_caja_desc_2"])
st.write(locale.textos["ayuda_cargar_caja_desc_3"])
st.image("./assets/helps/flujos_de_caja.png")

st.write(locale.textos["ayuda_cargar_caja_desc_4"])
st.image("./assets/helps/ahorro_exportar.png")

st.info(locale.textos["ayuda_cargar_ahorro_importante"])
