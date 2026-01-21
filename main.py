import pandas as pd
from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos

fichero = CargarFichero("raw/202512.xml")
fichero.parsear_xml()
fichero.limpiar_datos()

exportar = ExportarDatos(fichero)
exportar.exportar()

print("Todo el fichero parquet\n")
df = pd.read_parquet("data/finanzas.parquet")
print(df)

print("\nFichero parquet año 2025 y mes 12\n")
df_año = pd.read_parquet("data/finanzas.parquet", filters=[("año", "==", 2025), ("mes", "==", 12)])
print(df_año)
