import pandas as pd
from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos
from src.mis_finanzas import MisFinanzas

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

mis_finanzas = MisFinanzas(df, 11, 2025)
ingresos = mis_finanzas.obtener_ingresos_mes_año()
print(f"\nIngresos del mes: {ingresos}")
gastos = mis_finanzas.obtener_gastos_mes_año()
print(f"Gastos del mes: {gastos}")
print(f"Balance del mes: {ingresos + gastos}")
