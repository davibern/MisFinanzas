import streamlit as st

from src.locale import Locale


def main():
    locale = Locale(st.context.locale)
    inicio_pagina = st.Page("./pages/inicio.py", title=locale.textos["menu"]["inicio"], icon=":material/home:")
    cargar_datos = st.Page("./pages/cargar_datos.py", title=locale.textos["menu"]["cargar_datos"], icon=":material/file_upload:")
    resumen_mensual = st.Page("./pages/resumen_mensual.py", title=locale.textos["menu"]["resumen_mensual"], icon=":material/stacked_bar_chart:")
    resumen_anual = st.Page("./pages/resumen_anual.py", title=locale.textos["menu"]["resumen_anual"], icon=":material/bar_chart:")
    ahorro_prevision = st.Page("./pages/ahorro_prevision.py", title=locale.textos["menu"]["ahorro_prevision"], icon=":material/savings:")
    cargar_datos_ayuda = st.Page("./pages/cargar_datos_ayuda.py", title=locale.textos["menu"]["ayuda_cargar_datos"], icon=":material/help:")

    pg = st.navigation(
            {
                locale.textos["menu"]["inicio"]: [inicio_pagina],
                locale.textos["menu"]["informes"]: [resumen_mensual, resumen_anual, ahorro_prevision],
                locale.textos["menu"]["herramientas"]: [cargar_datos],
                locale.textos["menu"]["ayuda"]: [cargar_datos_ayuda]
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
