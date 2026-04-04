import streamlit as st
import os

from src.cargar_datos_caja import CargarFicheroCaja as CargarFichero
from src.exportar_datos import ExportarDatos
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("🗂️ " + locale.textos["titulo_cargar_caja"])

st.markdown(locale.textos["instrucciones_cargar_caja"])

st.write(locale.textos["ayuda_exportar_caja_texto"])
st.page_link("./pages/cargar_caja_ayuda.py", label=locale.textos["ayuda_exportar_caja_boton"], icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 2])
with col1:
    archivo = st.file_uploader(locale.textos["selecciona_archivo_csv"], type=['csv'])

if archivo is not None:
    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    exportar = ExportarDatos(fichero, tipo='caja')
    exportar.exportar_parquet()

    st.success(locale.textos["exito_cargar_caja"])

    with open(os.path.join(f"./raw/caja", archivo.name), "wb") as f:
        f.write(archivo.getbuffer())

    st.cache_data.clear()
    st.info(locale.textos["cache_limpiado"])