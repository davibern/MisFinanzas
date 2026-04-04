import streamlit as st
import os

from src.cargar_datos_ahorros import CargarFicheroAhorro as CargarFichero
from src.exportar_datos import ExportarDatos
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("🗂️ " + locale.textos["titulo_cargar_ahorro"])

st.markdown(locale.textos["instrucciones_cargar_ahorro"])

st.write(locale.textos["ayuda_exportar_ahorro_texto"])
st.page_link("./pages/cargar_ahorro_ayuda.py", label=locale.textos["ayuda_exportar_ahorro_boton"], icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 2])
with col1:
    archivo = st.file_uploader(locale.textos["selecciona_archivo_csv"], type=['csv'])

if archivo is not None:
    # Obtener el nombre de la compañia
    compañia = archivo.name.split('-')[1].strip().split(".")[0].strip()

    # Cargar y procesar el archivo desde el uploader de streamlit
    fichero = CargarFichero(archivo)
    fichero.limpiar_datos()

    exportar = ExportarDatos(fichero, tipo='ahorro', compañia=compañia)
    exportar.exportar_parquet()

    st.success(f'{locale.textos["exito_cargar_ahorro_1"]} {compañia} {locale.textos["exito_cargar_ahorro_2"]}')

    with open(os.path.join(f"./raw/{compañia.lower()}", archivo.name), "wb") as f:
        f.write(archivo.getbuffer())

    st.cache_data.clear()
    st.info(locale.textos["cache_limpiado"])
