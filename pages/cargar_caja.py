import streamlit as st
import os

from src.cargar_datos_caja import CargarFicheroCaja as CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos de Flujo de Caja")

st.markdown("""
1. Descarga el fichero de datos de tu NAS (Synology) en formato *.csv
2. Guardarlo en tu carpeta de descarga y seleccionalo con el botón de cargar.
""")

st.write("Si necesitas ayuda para exportar los datos de Flujo de Caja, puedes pulsar en el siguiente botón de ayuda 👇🏻")
st.page_link("./pages/cargar_caja_ayuda.py", label="Ayuda para exportar últimos movimientos", icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 2])
with col1:
    archivo = st.file_uploader('Selecciona un archivo CSV', type=['csv'])

if archivo is not None:
    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    exportar = ExportarDatos(fichero, tipo='caja')
    exportar.exportar_parquet()

    st.success(f'Datos de flujo de caja cargados correctamente y se ha guardado copia en /raw')

    with open(os.path.join(f"./raw/caja", archivo.name), "wb") as f:
        f.write(archivo.getbuffer())

    st.cache_data.clear()
    st.info("✅ Caché limpiado. Los nuevos datos estarán disponibles al navegar a otras páginas.")  