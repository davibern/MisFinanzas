import streamlit as st

st.title("📚 Manual de ayuda para importar datos de flujo de caja")
st.write("A continuación se detalla el proceso para descargar los datos de __Cargar Datos Caja__.")
st.markdown("""---""", unsafe_allow_html=True)

st.write("Entra en el fichero de datos económicos de tu Synology Nas, con tu usuario y contraseña.")
st.write("Una vez dentro seleccionamos la hoja de flujo de caja que deseamos descargar, en este caso, se __llama Flujo de caja__.")
st.image("./assets/helps/flujos_de_caja.png")

st.write("Una vez dentro pulsamos en el menú horizontal superior la opción Archivo y luego Descargar como, y por último ")
st.write("seleccionamos la opción __CSV__.")
st.image("./assets/helps/ahorro_exportar.png")

st.info("IMPORTANTE: No le cambies el nombre al fichero, éste ya incluye la compañía basada en el nombre de la hoja de Excel.")
