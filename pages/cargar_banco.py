import streamlit as st
import os

from src.cargar_datos_bancarios import CargarFicheroBancario as CargarFichero
from src.exportar_datos import ExportarDatos
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("🗂️ " + locale.textos["titulo_cargar_banco"])

st.markdown(locale.textos["instrucciones_cargar_banco"])

st.write(locale.textos["ayuda_exportar_banco_texto"])
st.page_link("./pages/cargar_banco_ayuda.py", label=locale.textos["ayuda_exportar_banco_boton"], icon="ℹ️")
st.markdown("""---""", unsafe_allow_html=True)

col1, _ = st.columns([1, 3])

with col1:
    nombre_archivo = str(st.text_input(locale.textos["nombre_archivo_banco_label"], placeholder=locale.textos["nombre_archivo_banco_placeholder"]))

# Validar que exista un nombre y luego que siga el formato correcto
if nombre_archivo:
    if nombre_archivo.isalpha():
        st.warning(locale.textos["error_formato_banco_numerico"])
    elif len(nombre_archivo) != 6:
        st.warning(locale.textos["error_formato_banco_longitud"])
    else:

        col1, _ = st.columns([1, 2])

        with col1:
            archivo = st.file_uploader(locale.textos["selecciona_archivo_xml"], type=["xml"])

        if archivo is not None:
            # Cargar y procesar el archivo desde el uploader de Streamlit
            fichero = CargarFichero(archivo)
            fichero.parsear_xml()
            fichero.limpiar_datos()
            exportar = ExportarDatos(fichero, tipo="bancario")
            resultado = exportar.exportar_parquet()

            # Comprobar resultado
            if resultado == 0:
                st.warning(locale.textos["aviso_banco_procesado"])
            else:
                # Crear directorio raw si no existe
                if not os.path.exists("./raw/bancario"):
                    os.makedirs("./raw/bancario")

                # Guardar el archivo original en la carpeta raw como copia de seguridad con el nombre indicado
                nombre_archivo = f"{nombre_archivo}.xml" if nombre_archivo else archivo.name
                with open(os.path.join("./raw/bancario", nombre_archivo), "wb") as f:
                    f.write(archivo.getbuffer())
                st.success(locale.textos["exito_cargar_banco"])
                st.cache_data.clear()
                st.info(locale.textos["cache_limpiado"])
