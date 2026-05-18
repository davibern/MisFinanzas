import streamlit as st
import os

from src.cargar_datos_bancarios import CargarFicheroBancario
from src.cargar_datos_caja import CargarFicheroCaja
from src.cargar_datos_ahorros import CargarFicheroAhorro
from src.exportar_datos import ExportarDatos
from src.locale import Locale

locale = Locale(st.context.locale)

st.title("🗂️ " + locale.textos['titulo_cargar_datos'])

# Pestañas
tab_banco, tab_caja, tab_ahorro = st.tabs(["Banco", "Caja", "Ahorro"])

with tab_banco:
    st.header(f"{locale.textos['titulo_cargar_banco']}")
    st.markdown(locale.textos["instrucciones_cargar_banco"])

    st.write(locale.textos["ayuda_exportar_banco_texto"])
    st.page_link("./pages/cargar_datos_ayuda.py", label=locale.textos["ayuda_exportar_banco_boton"], icon="ℹ️")
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
                archivo = st.file_uploader(locale.textos["selecciona_archivo_xml"], type=["xml"], key="uploader_banco")

            if archivo is not None:
                # Cargar y procesar el archivo desde el uploader de Streamlit
                fichero = CargarFicheroBancario(archivo)
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

with tab_caja:
    st.header(f"{locale.textos['titulo_cargar_caja']}")

    st.markdown(locale.textos["instrucciones_cargar_caja"])

    st.write(locale.textos["ayuda_exportar_caja_texto"])
    st.page_link("./pages/cargar_datos_ayuda.py", label=locale.textos["ayuda_exportar_caja_boton"], icon="ℹ️")
    st.markdown("""---""", unsafe_allow_html=True)

    col1, _ = st.columns([1, 2])
    with col1:
        archivo = st.file_uploader(locale.textos["selecciona_archivo_csv"], type=['csv'], key="uploader_caja")

    if archivo is not None:
        # Cargar y procesar el archivo desde el uploader de streamlit
        fichero = CargarFicheroCaja(archivo)
        fichero.limpiar_datos()

        exportar = ExportarDatos(fichero, tipo='caja')
        exportar.exportar_parquet()

        st.success(locale.textos["exito_cargar_caja"])

        with open(os.path.join(f"./raw/caja", archivo.name), "wb") as f:
            f.write(archivo.getbuffer())

        st.cache_data.clear()
        st.info(locale.textos["cache_limpiado"])

with tab_ahorro:
    st.header(f"{locale.textos['titulo_cargar_ahorro']}")

    st.markdown(locale.textos["instrucciones_cargar_ahorro"])

    st.write(locale.textos["ayuda_exportar_ahorro_texto"])
    st.page_link("./pages/cargar_datos_ayuda.py", label=locale.textos["ayuda_exportar_ahorro_boton"], icon="ℹ️")
    st.markdown("""---""", unsafe_allow_html=True)

    col1, _ = st.columns([1, 2])
    with col1:
        archivo = st.file_uploader(locale.textos["selecciona_archivo_csv"], type=['csv'], key="uploader_ahorro")

    if archivo is not None:
        # Obtener el nombre de la compañia
        compañia = archivo.name.split('-')[1].strip().split(".")[0].strip()

        # Cargar y procesar el archivo desde el uploader de streamlit
        fichero = CargarFicheroAhorro(archivo)
        fichero.limpiar_datos()

        exportar = ExportarDatos(fichero, tipo='ahorro', compañia=compañia)
        exportar.exportar_parquet()

        st.success(f'{locale.textos["exito_cargar_ahorro_1"]} {compañia} {locale.textos["exito_cargar_ahorro_2"]}')

        os.makedirs(f"./raw/{compañia.lower()}", exist_ok=True)
        with open(os.path.join(f"./raw/{compañia.lower()}", archivo.name), "wb") as f:
            f.write(archivo.getbuffer())

        st.cache_data.clear()
        st.info(locale.textos["cache_limpiado"])
