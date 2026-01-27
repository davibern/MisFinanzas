import streamlit as st
from PIL import Image

st.title("📊 Mis Finanzas")
image = Image.open("./assets/logo.png")
st.image(image, width=900)
st.write("Bienvenido a la página de inicio de Mis Finanzas.")
st.write("Aquí puedes gestionar y analizar tus finanzas personales de manera eficiente.")
