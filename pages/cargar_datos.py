import streamlit as st
import os

from src.cargar_fichero import CargarFicheroBancario as CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos")

st.markdown("""
1. Indica el **año y el mes** del archivo que se va a cargar. Sigue el formato indicado (YYYYMM)
2. Seguidamente, selecciona el archivo `.xml` que se va a cargar.
""")

st.write("Si necesitas ayuda para exportar los datos de CaixaBank, puedes pulsar el siguiente botón de ayuda 👇🏻")
st.page_link("./pages/cargar_datos_ayuda.py", label="Ayuda para exportar últimos movimientos", icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 3])

with col1:
    nombre_archivo = str(st.text_input("Nombre del archivo (formato: YYYYMM)", placeholder="YYYYMM"))

# Validar que exista un nombre y luego que siga el formato correcto
if nombre_archivo:
    if nombre_archivo.isalpha():
        st.warning("El nombre del fichero debe ser numérico y seguir el formato YYYYMM, ejemplo: 202401, que sería enero 2024.")
    elif len(nombre_archivo) != 6:
        st.warning("El nombre del fichero debe tener 6 dígitos y seguir el formato YYYYMM, ejemplo: 202401, que sería enero 2024.")
    else:

        col1, _ = st.columns([1, 2])

        with col1:
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
                if not os.path.exists("./raw/bancario"):
                    os.makedirs("./raw/bancario")

                # Guardar el archivo original en la carpeta raw como copia de seguridad con el nombre indicado
                nombre_archivo = f"{nombre_archivo}.xml" if nombre_archivo else archivo.name
                with open(os.path.join("./raw/bancario", nombre_archivo), "wb") as f:
                    f.write(archivo.getbuffer())
                st.success("Datos exportados correctamente. Se ha guardado una copia en la carpeta raw y los datos se han añadido al parquet.")
                st.cache_data.clear()
                st.info("✅ Caché limpiado. Los nuevos datos estarán disponibles al navegar a otras páginas.")
