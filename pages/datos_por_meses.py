import streamlit as st
import plotly.graph_objects as go

from src.mis_finanzas import MisFinanzas

# Título de la página
st.title("📅 Datos por Meses")
st.write("Histograma de datos financieros agrupados por meses, con gráficos y estadísticas.")
st.write("Selecciona el año y el mes para obtener los datos correspondientes, y obtendrás\
    automáticamente la evolución de los últimos doce meses.")
st.write("Encontrarás además un desglose de gastos e ingresos por categoría.")

# Cargar datos
datos = MisFinanzas()


def selector_año_mes() -> None:
    """Selector de año y mes"""
    st.markdown("---")
    st.markdown("#### Selecciona el año y el mes que deseas consultar")
    col1, col2 = st.columns(2)
    with col1:
        global año
        año = st.selectbox("Año", range(2024, 2026), index=1)
    with col2:
        global mes
        mes = st.selectbox("Mes", range(1, 13), index=11)
    st.markdown("---")


selector_año_mes()
