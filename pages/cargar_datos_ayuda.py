import streamlit as st

st.title("📚 Manual de ayuda para importar datos bancarios")
st.write("A continuación se detalla el proceso para descargar los datos de la cuenta de CaixaBank para que puedas importarlo en la herramienta de __Cargar Datos__.")
st.markdown("""---""", unsafe_allow_html=True)

st.write("Entramos en https://www.caixabank.es/, con nuestro usuario y contraseña.")
st.write("Una vez dentro pulsamos en el menú horizontal, en la opción cuentas y tarjetas y luego en mis finanzas.")
st.image("./assets/helps/cuentas_tarjetas_mis_finanzas.png")

st.write("Una vez dentro buscamos el cuadro de movimientos y pulsamos en el título del mismo para ver todos los movimientos.")
st.image("./assets/helps/ultimos_movimientos.png")

st.write("Esto nos llevará a la página de movimientos, aquí tenemos que filtrar el mes que queramos añadir a __Mis Finanzas__.")
st.write("Para ello pulsamos en __Periodo__ seleccionamos el mes, normalmente el mes anterior, y pulsamos en el botón azul __Filtrar__.")
st.image("./assets/helps/seleccionar_mes.png")

st.write("Ahora, el paso importante es __listar todos los movimientos del mes en cuestión para que estén disponibles en la pantalla__.")
st.write("Para ello con el ratón buscamos un texto con un enlace llamado __ver mas movimientos__ y lo pulsamos tantas veces como necesitemos para mostrar el primer movimiento del mes.")
st.image("./assets/helps/ver_mas_movimientos.png")

st.write("Ahora que están en la pantalla todos los datos disponibles (ingresos y gastos del mes seleccionado) lo siguiente es volver a la parte de arriba de la página y pulsar en el botón de la esquina superior derecha llamada __exportar__.")
st.image("./assets/helps/exportar.png")

st.write("Por último, seleccionamos la opción __lista de movimientos visualizados en pantalla__ y pulsamos en __aceptar__ y se descargará un fichero .xlm")
st.image("./assets/helps/exportar_lista_movimientos.png")