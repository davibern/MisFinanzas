from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos
import pandas as pd

fichero = CargarFichero("raw/202512.xml")
fichero.parsear_xml()
fichero.limpiar_datos()

exportar = ExportarDatos(fichero)
exportar.exportar()

df = pd.read_parquet("data/finanzas.parquet")
print(df)