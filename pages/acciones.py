import streamlit as st

from src.locale import Locale

# Obtener el idioma del contexto
locale = Locale(st.context.locale)

# Título de la página
st.title("📈 " + locale.textos["titulo_accion"])
