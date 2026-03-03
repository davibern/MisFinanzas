import streamlit as st

from src.cargar_datos_ahorros import CargarFicheroAhorro as CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos de Ahorro")

archivo = st.file_uploader('Selecciona un archivo CSV', type=['csv'])

if archivo is not None:
    # Obtener el nombre de la compañia
    compañia = archivo.name.split('-')[1].strip().split(".")[0].strip()

    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    exportar = ExportarDatos(fichero, tipo='ahorro', compañia=compañia)
    exportar.exportar_parquet()

    st.dataframe(fichero.df)
