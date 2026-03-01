import streamlit as st

from src.cargar_datos_ahorros import CargarDatosAhorros as CargarFichero

st.title("🗂️ Cargar Datos de Ahorro")

archivo = st.file_uploader('Selecciona un archivo CSV', type=['csv'])

if archivo is not None:
    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    st.dataframe(fichero.df)
