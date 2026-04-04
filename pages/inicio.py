import streamlit as st

from src.locale import Locale
from PIL import Image

# Obtener el idioma del contexto (ejemplo: "es", "en")
locale = Locale(st.context.locale)

st.title("📊 " + locale.textos["nombre_app"])
image = Image.open("./assets/logo.webp")
st.image(image, width=900)
st.write(locale.textos["mensaje_inicio_1"])
st.write(locale.textos["mensaje_inicio_2"])
