from src.cargar_fichero import CargarFichero
from src.exportar_datos import ExportarDatos
from src.mis_finanzas import MisFinanzas

cargar: bool = False
if cargar:
    for mes in range(1, 13):
        fichero = CargarFichero(f"raw/2025{mes:02d}.xml")
        fichero.parsear_xml()
        fichero.limpiar_datos()
        exportar = ExportarDatos(fichero)
        exportar.exportar()

mes_11 = MisFinanzas()
ingresos_11 = mes_11.obtener_ingresos_mes_año(2025, 11)
gastos_11 = mes_11.obtener_gastos_mes_año(2025, 11)
mes_12 = MisFinanzas()
ingresos_12 = mes_12.obtener_ingresos_mes_año(2025, 12)
gastos_12 = mes_12.obtener_gastos_mes_año(2025, 12)
print(f"\nIngresos del mes 11: {ingresos_11}")
print(f"\nGastos del mes 11: {gastos_11}")
print(f"\nIngresos del mes 12: {ingresos_12}")
print(f"\nGastos del mes 12: {gastos_12}")

finanzas = MisFinanzas()
intervalo_gastos = finanzas.obtener_intervalo_gastos(2025, 11, 12)
intervalo_ingresos = finanzas.obtener_intervalo_ingresos(2025, 11, 12)
print(intervalo_gastos)
print(intervalo_ingresos)

mes_estudio = MisFinanzas()
gastos_categoria = mes_estudio.obtener_ingresos_agrupados_mes_año(2025, 12)
print(gastos_categoria)

ingresos_mensuales = finanzas.obtener_intervalo_ingresos_por_meses(2025)
print(ingresos_mensuales)
