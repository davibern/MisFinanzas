import streamlit as st
import plotly.graph_objects as go

from datetime import datetime
from src.mis_finanzas import MisFinanzas
from src.mis_cajas import MisCajas
from src.enums import Mes
from src.config import Color
from src.locale import Locale


# Obtener el idioma del contexto (ejemplo: "es", "en")
locale = Locale(st.context.locale)

# Título de la página
st.title(locale.textos["titulo_resumen_anual"])
st.write(locale.textos["descripcion_resumen_anual"])

# Mapear número de mes a nombre en español
nombres_meses = Mes.get_map_dict()

# Cargar datos
datos = MisFinanzas()
cajas = MisCajas()


def selector_año() -> None:
    """Selector de año y mes"""
    st.markdown("---")
    col1, _ = st.columns([1, 3])
    with col1:
        global año
        años = list(range(datos.obtener_año_minimo(), datos.obtener_año_maximo() + 1))
        año_actual = datetime.now().year

        # Calculo el índice del año actual en la lista de años
        # Si el año actual no está en la lista, uso 0 para evitar errores
        try:
            indice_defecto_año = años.index(año_actual)
        except ValueError:
            indice_defecto_año = 0
        año = st.selectbox(locale.textos["opcion"]["año"], años, index=indice_defecto_año, help=locale.textos["opcion"]["selecciona_año"])
    st.markdown("---")


def obtener_intervalo_ingresos_meses() -> None:
    """
    Obtiene la suma de los ingresos por meses
    """
    st.subheader(locale.textos["ingresos_gastos_mes"])

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
    st.markdown("---")


def obtener_historico_flujo_caja() -> None:
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')    
    with col1:
        st.subheader(locale.textos["historico_flujo_caja"])

        fig = go.Figure()
        historico_flujo_caja = cajas.obtener_historico()

        fig.add_trace(
            go.Scatter(
                x=historico_flujo_caja['FECHA'],
                y=historico_flujo_caja['CAJA'],
                mode='lines+markers',
                name='Flujo de caja',
                line=dict(color=Color.AZUL),
                marker=dict(color=Color.AZUL),
            )
        )

        st.plotly_chart(fig, width='stretch')

    with col3:
        st.metric(label=locale.textos["media_flujo_caja_3"], value=f"{cajas.obtener_media_caja_3_meses():.2f} €")
        st.metric(label=locale.textos["media_flujo_caja_6"], value=f"{cajas.obtener_media_caja_6_meses():.2f} €")
        st.metric(label=locale.textos["media_flujo_caja_12"], value=f"{cajas.obtener_media_caja_12_meses():.2f} €")


selector_año()
obtener_intervalo_ingresos_meses()
obtener_historico_flujo_caja()  
