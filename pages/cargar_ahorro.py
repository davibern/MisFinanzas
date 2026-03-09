import streamlit as st
import os

from src.cargar_datos_ahorros import CargarFicheroAhorro as CargarFichero
from src.exportar_datos import ExportarDatos

st.title("🗂️ Cargar Datos de Ahorro")

st.markdown("""
1. Descarga el fichero de datos de tu NAS (Synology) en formato *.csv
2. Guardarlo en tu carpeta de descarga y seleccionalo con el botón de cargar.
""")

st.write("Si necesitas ayuda para exportar los datos de Ahorro, puedes pulsar en el siguiente botónde ayuda 👇🏻")
st.page_link("./pages/cargar_ahorro_ayuda.py", label="Ayuda para exportar últimos movimientos", icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 2])
with col1:
    archivo = st.file_uploader('Selecciona un archivo CSV', type=['csv'])

if archivo is not None:
    # Obtener el nombre de la compañia
    compañia = archivo.name.split('-')[1].strip().split(".")[0].strip()

    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    exportar = ExportarDatos(fichero, tipo='ahorro', compañia=compañia)
    exportar.exportar_parquet()

    st.success(f'Datos de ahorro de {compañia} cargados correctamente y se ha guardado copia en /raw')

    with open(os.path.join(f"./raw/{compañia.lower()}", archivo.name), "wb") as f:
        f.write(archivo.getbuffer())

    st.cache_data.clear()
    st.info("✅ Caché limpiado. Los nuevos datos estarán disponibles al navegar a otras páginas.")
