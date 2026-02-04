import streamlit as st


def main():
    inicio_pagina = st.Page("./pages/inicio.py", title="Inicio", icon=":material/home:")
    cargar_pagina = st.Page("./pages/cargar_datos.py", title="Cargar Datos", icon=":material/file_upload:")
    resumen_mensual = st.Page("./pages/resumen_mensual.py", title="Resumen Mensual", icon=":material/stacked_bar_chart:")
    resumen_anual = st.Page("./pages/resumen_anual.py", title="Resumen Anual", icon=":material/bar_chart:")

    pg = st.navigation(
            {
                "Inicio": [inicio_pagina],
                "Informes": [resumen_mensual, resumen_anual],
                "Herramientas": [cargar_pagina],
            }
        )

    st.set_page_config(
        page_title="Mis Finanzas",
        page_icon=":material/account_balance_wallet:",
        layout="wide"
    )

    pg.run()


if __name__ == "__main__":
    main()
