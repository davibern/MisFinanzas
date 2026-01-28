import streamlit as st
import os

from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos")

st.markdown("""
1. Lo primero es indicar el **año y el mes** del archivo que se va a cargar.
    - Esto servirá para almacenar la copia de seguridad del archivo original con el nombre que indiques en `/raw`.
2. A continuación, se debe seleccionar el archivo `.xml` que se va a cargar.
""")

nombre_archivo = st.text_input("Nombre del archivo (formato: YYYYMM)")

if nombre_archivo:
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
