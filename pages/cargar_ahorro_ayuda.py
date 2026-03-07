import streamlit as st

st.title("📚 Manual de ayuda para importar datos bancarios")
st.write("A continuación se detalla el proceso para descargar los datos de la cuenta de CaixaBank para \
    que puedas importarlo en la herramienta de __Cargar Datos Ahorro__.")
st.markdown("""---""", unsafe_allow_html=True)

st.write("Entramos en https://davibernas.quickconnect.to/oo/r/uczNKWLm3qjwKxO6zxOGG8QRKhgHtLHG, con nuestro usuario y contraseña.")
st.write("Una vez dentro seleccionamos la hoja de la aseguradora que deseamos descargar")
st.image("./assets/helps/ahorro_aseguradoras.png")

st.write("Una vez dentro pulsamos en el menú horizontal superior la opción Archivo y luego Descargar como, y por último \
    seleccionamos la opción __CSV__.")
st.image("./assets/helps/ahorro_exportar.png")

st.info("IMPORTANTE: No le cambies el nombre al fichero, éste ya incluye la compañía basada en el nombre de la hoja de Excel.")
