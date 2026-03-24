import streamlit as st
import plotly.graph_objects as go

from datetime import datetime
from src.mis_finanzas import MisFinanzas
from src.enums import Mes
from src.config import Color

# Título de la página
st.title("📅 Datos por Meses")
st.write("Histograma de gastos vs ingresos por mes en el año seleccionado.")

# Mapear número de mes a nombre en español
nombres_meses = Mes.get_map_dict()

# Cargar datos
datos = MisFinanzas()


def selector_año() -> None:
    """Selector de año y mes"""
    st.markdown("---")
    col1, _ = st.columns([1, 3])
    with col1:
        global año
        años = list(range(2024, 2027))
        año_actual = datetime.now().year

        # Calculo el índice del año actual en la lista de años
        # Si el año actual no está en la lista, uso 0 para evitar errores
        try:
            indice_defecto_año = años.index(año_actual)
        except ValueError:
            indice_defecto_año = 0
        año = st.selectbox("Año", años, index=indice_defecto_año, help="Selecciona el año que deseas consultar")
    st.markdown("---")


def obtener_intervalo_ingresos_meses() -> None:
    """
    Obtiene la suma de los ingresos por meses
    """
    fig = go.Figure()
    ingresos_meses = datos.obtener_intervalo_ingresos_por_meses(año)
    gastos_meses = datos.obtener_intervalo_gastos_por_meses(año).abs()

    # Mapear número de mes a nombre en español
    ingresos_meses['mes_nombre'] = ingresos_meses['mes'].map(nombres_meses)
    gastos_meses['mes_nombre'] = gastos_meses['mes'].map(nombres_meses)

    fig.add_trace(
        go.Scatter(
            x=ingresos_meses['mes_nombre'],
            y=ingresos_meses['importe'],
            mode='lines+markers',
            name='Ingresos',
            line=dict(color=Color.AZUL),
            marker=dict(color=Color.AZUL),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=gastos_meses['mes_nombre'],
            y=gastos_meses['importe'],
            mode='lines+markers',
            name='Gastos',
            line=dict(color=Color.ROJO),
            marker=dict(color=Color.ROJO),
        )
    )

    st.plotly_chart(fig, width='stretch')


selector_año()
obtener_intervalo_ingresos_meses()
