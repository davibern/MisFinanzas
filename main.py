from cargar_fichero import CargarFichero

fichero = CargarFichero("files/202512.xml")
fichero.parsear_xml()
fichero.limpiar_datos()
print(fichero.df)