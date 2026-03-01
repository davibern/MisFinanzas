import streamlit as st


def main():
    inicio_pagina = st.Page("./pages/inicio.py", title="Inicio", icon=":material/home:")
    cargar_banco = st.Page("./pages/cargar_banco.py", title="Cargar Banco", icon=":material/file_upload:")
    cargar_ahorro = st.Page("./pages/cargar_ahorro.py", title="Cargar Ahorro", icon=":material/file_upload:")
    resumen_mensual = st.Page("./pages/resumen_mensual.py", title="Resumen Mensual", icon=":material/stacked_bar_chart:")
    resumen_anual = st.Page("./pages/resumen_anual.py", title="Resumen Anual", icon=":material/bar_chart:")
    ahorro_prevision = st.Page("./pages/ahorro_prevision.py", title="Ahorro y Previsión", icon=":material/savings:")
    cargar_banco_ayuda = st.Page("./pages/cargar_banco_ayuda.py", title="Ayuda datos bancarios", icon=":material/help:")

    pg = st.navigation(
            {
                "Inicio": [inicio_pagina],
                "Informes": [resumen_mensual, resumen_anual, ahorro_prevision],
                "Herramientas": [cargar_banco, cargar_ahorro],
                "Ayuda": [cargar_banco_ayuda]
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
