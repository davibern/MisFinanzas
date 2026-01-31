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


def obtener_intervalo_ingresos_meses() -> None:
    """
    Obtiene la suma de los ingresos por meses
    """
    fig = go.Figure()
    ingresos_meses = datos.obtener_intervalo_ingresos_por_meses(año)
    gastos_meses = datos.obtener_intervalo_gastos_por_meses(año).abs()
    fig.add_trace(
        go.Scatter(
            x=ingresos_meses['mes'],
            y=ingresos_meses['importe'],
            mode='lines+markers',
            name='Ingresos',
            line=dict(color='#1f77b4'),
            marker=dict(color='#1f77b4'),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gastos_meses['mes'],
            y=gastos_meses['importe'],
            mode='lines+markers',
            name='Gastos',
            line=dict(color='#d62728'),
            marker=dict(color='#d62728'),
        )
    )

    st.plotly_chart(fig, use_container_width=True)


selector_año_mes()
obtener_intervalo_ingresos_meses()
