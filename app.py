import streamlit as st

inicio_pagina = st.Page("./pages/inicio.py", title="Inicio", icon=":material/home:")
cargar_pagina = st.Page("./pages/cargar_datos.py", title="Cargar Datos", icon=":material/file_upload:")
datos_mes_pagina = st.Page("./pages/datos_por_mes.py", title="Datos del Mes", icon=":material/calendar_month:")

pg = st.navigation(
        {
            "Inicio": [inicio_pagina],
            "Informes": [datos_mes_pagina],
            "Herramientas": [cargar_pagina],
        }
    )
st.set_page_config(page_title="Mis Funciones", page_icon=":material/leaderboard:", layout="wide")

pg.run()
