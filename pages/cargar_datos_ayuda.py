import streamlit as st
from src.locale import Locale

locale = Locale(st.context.locale)

tab_banco, tab_caja, tab_ahorro = st.tabs(["Banco", "Caja", "Ahorro"])

with tab_banco:
    st.title("📚 " + locale.textos["titulo_ayuda_cargar_banco"])
    st.write(locale.textos["ayuda_cargar_banco_desc_1"])
    st.markdown("""---""", unsafe_allow_html=True)

    st.write(locale.textos["ayuda_cargar_banco_desc_2"])
    st.write(locale.textos["ayuda_cargar_banco_desc_3"])
    st.image("./assets/helps/cuentas_tarjetas_mis_finanzas.png")

    st.write(locale.textos["ayuda_cargar_banco_desc_4"])
    st.image("./assets/helps/ultimos_movimientos.png")

    st.write(locale.textos["ayuda_cargar_banco_desc_5"])
    st.write(locale.textos["ayuda_cargar_banco_desc_6"])
    st.image("./assets/helps/seleccionar_mes.png")

    st.info(locale.textos["ayuda_cargar_banco_importante_1"])

    st.write(locale.textos["ayuda_cargar_banco_desc_7"])
    st.write(locale.textos["ayuda_cargar_banco_desc_8"])
    st.image("./assets/helps/ver_mas_movimientos.png")

    st.write(locale.textos["ayuda_cargar_banco_desc_9"])
    st.image("./assets/helps/exportar.png")

    st.write(locale.textos["ayuda_cargar_banco_desc_10"])
    st.image("./assets/helps/exportar_lista_movimientos.png")

with tab_caja:
    st.title("📚 " + locale.textos["titulo_ayuda_cargar_caja"])
    st.write(locale.textos["ayuda_cargar_caja_desc_1"])
    st.markdown("""---""", unsafe_allow_html=True)

    st.write(locale.textos["ayuda_cargar_caja_desc_2"])
    st.write(locale.textos["ayuda_cargar_caja_desc_3"])
    st.image("./assets/helps/flujos_de_caja.png")

    st.write(locale.textos["ayuda_cargar_caja_desc_4"])
    st.image("./assets/helps/ahorro_exportar.png")

    st.info(locale.textos["ayuda_cargar_ahorro_importante"])

with tab_ahorro:
    st.title("📚 " + locale.textos["titulo_ayuda_cargar_ahorro"])
    st.write(locale.textos["ayuda_cargar_ahorro_desc_1"])
    st.markdown("""---""", unsafe_allow_html=True)

    st.write(locale.textos["ayuda_cargar_ahorro_desc_2"])
    st.write(locale.textos["ayuda_cargar_ahorro_desc_3"])
    st.image("./assets/helps/ahorro_aseguradoras.png")

    st.write(locale.textos["ayuda_cargar_ahorro_desc_4"])
    st.image("./assets/helps/ahorro_exportar.png")

    st.info(locale.textos["ayuda_cargar_ahorro_importante"])
