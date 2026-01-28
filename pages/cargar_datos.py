import streamlit as st
import os

from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos")

st.write("Por favor, selecciona un archivo XML para cargar en la fuente de datos.")
st.write("Escribe a continuación el nombre con el que se guardará la copia original")

nombre_archivo = st.text_input("Nombre del archivo (formato: YYYYMM)")

archivo = st.file_uploader("Selecciona un archivo XML", type=["xml"])

if archivo is not None:
    # Cargar y procesar el archivo desde el uploader de Streamlit
    fichero = CargarFichero(archivo)
    fichero.parsear_xml()
    fichero.limpiar_datos()
    exportar = ExportarDatos(fichero)
    resultado = exportar.exportar()

    # Comprobar resultado
    if resultado == 0:
        st.warning("El año y el mes ya han sido procesados anteriormente.")
    else:
        # Crear directorio raw si no existe
        if not os.path.exists("./raw"):
            os.makedirs("./raw")

        # Guardar el archivo original en la carpeta raw como copia de seguridad con el nombre indicado
        nombre_archivo = f"{nombre_archivo}.xml" if nombre_archivo else archivo.name
        with open(os.path.join("./raw", nombre_archivo), "wb") as f:
            f.write(archivo.getbuffer())
        st.success("Datos exportados correctamente. Se ha guardado una copia en la carpeta raw y los datos se han añadido al parquet.")
