import streamlit as st

from src.locale import Locale


def main():
    locale = Locale(st.context.locale)
    inicio_pagina = st.Page("./pages/inicio.py", title=locale.textos["menu"]["inicio"], icon=":material/home:")
    cargar_banco = st.Page("./pages/cargar_banco.py", title=locale.textos["menu"]["cargar_banco"], icon=":material/file_upload:")
    cargar_ahorro = st.Page("./pages/cargar_ahorro.py", title=locale.textos["menu"]["cargar_ahorro"], icon=":material/file_upload:")
    cargar_caja = st.Page("./pages/cargar_caja.py", title=locale.textos["menu"]["cargar_caja"], icon=":material/file_upload:")
    resumen_mensual = st.Page("./pages/resumen_mensual.py", title=locale.textos["menu"]["resumen_mensual"], icon=":material/stacked_bar_chart:")
    resumen_anual = st.Page("./pages/resumen_anual.py", title=locale.textos["menu"]["resumen_anual"], icon=":material/bar_chart:")
    ahorro_prevision = st.Page("./pages/ahorro_prevision.py", title=locale.textos["menu"]["ahorro_prevision"], icon=":material/savings:")
    cargar_banco_ayuda = st.Page("./pages/cargar_banco_ayuda.py", title=locale.textos["menu"]["ayuda_datos_banarios"], icon=":material/help:")
    cargar_ahorro_ayuda = st.Page("./pages/cargar_ahorro_ayuda.py", title=locale.textos["menu"]["ayuda_datos_ahorro"], icon=":material/help:")
    cargar_caja_ayuda = st.Page("./pages/cargar_caja_ayuda.py", title=locale.textos["menu"]["ayuda_datos_caja"], icon=":material/help:")

    pg = st.navigation(
            {
                locale.textos["menu"]["inicio"]: [inicio_pagina],
                locale.textos["menu"]["informes"]: [resumen_mensual, resumen_anual, ahorro_prevision],
                locale.textos["menu"]["herramientas"]: [cargar_banco, cargar_ahorro, cargar_caja],
                locale.textos["menu"]["ayuda"]: [cargar_banco_ayuda, cargar_ahorro_ayuda, cargar_caja_ayuda]
            }
        )

    st.set_page_config(
        page_title=locale.textos["nombre_app"],
        page_icon=":material/account_balance_wallet:",
        layout="wide"
    )

    pg.run()


if __name__ == "__main__":
    main()
