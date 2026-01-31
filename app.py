import streamlit as st


def main():
    inicio_pagina = st.Page("./pages/inicio.py", title="Inicio", icon=":material/home:")
    cargar_pagina = st.Page("./pages/cargar_datos.py", title="Cargar Datos", icon=":material/file_upload:")
    datos_mes_pagina = st.Page("./pages/datos_por_mes.py", title="Resumen Mensual", icon=":material/stacked_bar_chart:")
    datos_por_meses = st.Page("./pages/datos_por_meses.py", title="Datos por Meses", icon=":material/bar_chart:")

    pg = st.navigation(
            {
                "Inicio": [inicio_pagina],
                "Informes": [datos_mes_pagina, datos_por_meses],
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
