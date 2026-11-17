import streamlit as st

from src.locale import Locale
from PIL import Image
from pathlib import Path

# Obtener el idioma del contexto (ejemplo: "es", "en")
locale = Locale(st.context.locale)

st.title("📊 " + locale.textos["nombre_app"])
image = Image.open("./assets/logo.webp")
st.image(image, width=900)

ruta_raiz = Path(__file__).resolve().parent.parent
ruta_archivo = ruta_raiz / "version"

version = ruta_archivo.read_text(encoding="utf-8")
st.write(version)
