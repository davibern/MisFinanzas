import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime
from src.mis_finanzas import MisFinanzas
from src.mis_ahorros import MisAhorros

# Título de la página
st.title("💰 Ahorro y Previsión")
st.write("Histograma del ahorro mensual en el año seleccionado.")
st.write("Selecciona el año para obtener los datos correspondientes, y obtendrás\
    automáticamente la evolución de los últimos doce meses.")

# Mapear número de mes a nombre en español
nombres_meses = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Cargar datos de finanzas y ahorros
finanzas = MisFinanzas()
ahorros_axa = MisAhorros('axa')
ahorros_fiatc = MisAhorros('fiatc')


def selector_año() -> None:
    """Selector de año y mes"""
    st.markdown("---")
    st.markdown("#### Selecciona el año y el mes que deseas consultar")
    col1, col2 = st.columns(2)
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
        año = st.selectbox("Año", años, index=indice_defecto_año)
    st.markdown("---")


def obtener_intervalo_ahorro_meses() -> None:
    """
    Obtiene la diferencia entre los gastos e ingresos por meses
    """
    df_ingresos = finanzas.obtener_intervalo_ingresos_por_meses(año)
    df_gastos = finanzas.obtener_intervalo_gastos_por_meses(año)

    df_final = pd.merge(df_ingresos, df_gastos, on='mes', suffixes=('_ingresos', '_gastos'))
    df_final['diferencia'] = df_final['importe_ingresos'] + df_final['importe_gastos']
    df_final['ahorrado'] = df_final['diferencia'] > 0

    # Mapear número de mes a nombre en español
    df_final['mes_nombre'] = df_final['mes'].map(nombres_meses)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_final['mes_nombre'],
            y=df_final['diferencia'],
            mode='lines+markers',
            name='Ahorro'
        )
    )

    st.plotly_chart(fig, width='stretch')


def obtener_total_diferencia() -> None:
    """
    Obtiene el total de las diferencias de ingresos y gastos del año completo
    """
    total_ingresos = finanzas.obtener_intervalo_ingresos_por_meses(año)['importe'].sum()
    total_gastos = finanzas.obtener_intervalo_gastos_por_meses(año)['importe'].sum()
    total_diferencia = total_ingresos + total_gastos

    st.metric(label="Ahorro total del año", value=f"{total_diferencia:.2f} €")


def obtener_media_diferencia() -> None:
    """
    Obtiene el promedio de las diferencias entre gasto e ingresos del año completo
    """
    df_ingresos = finanzas.obtener_intervalo_ingresos_por_meses(año)
    df_gastos = finanzas.obtener_intervalo_gastos_por_meses(año)

    df_final = pd.merge(df_ingresos, df_gastos, on='mes', suffixes=('_ingresos', '_gastos'))
    df_final['diferencia'] = df_final['importe_ingresos'] + df_final['importe_gastos']
    df_final['ahorrado'] = df_final['diferencia'] > 0

    media_diferencia = df_final['diferencia'].mean()
    st.metric(label="Ahorro medio mensual", value=f"{media_diferencia:.2f} €")


def obtener_intervalo_tasa_ahorro() -> None:
    """
    Obtiene la tasa de ahorro con respecto a los ingresos: ((ingresos - gastos) / ingresos) * 100
    """
    df_ingresos = finanzas.obtener_intervalo_ingresos_por_meses(año)
    df_gastos = finanzas.obtener_intervalo_gastos_por_meses(año)

    df_final = pd.merge(df_ingresos, df_gastos, on='mes', suffixes=('_ingresos', '_gastos'))
    df_final['diferencia'] = df_final['importe_ingresos'] + df_final['importe_gastos']
    df_final['tasa_ahorro'] = (df_final['diferencia'] / df_final['importe_ingresos'] * 100).round(2)

    # Mapear número de mes a nombre en español
    df_final['mes_nombre'] = df_final['mes'].map(nombres_meses)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_final['mes_nombre'],
            y=df_final['tasa_ahorro'],
            mode='lines+markers',
            name='Tasa de Ahorro (%)'
        )
    )

    st.plotly_chart(fig, width='stretch')


def obtener_media_tasa_ahorro() -> None:
    """
    Obtiene la tasa de ahorro medio con respecto a los ingresos: ((ingresos - gastos) / ingresos) * 100
    """
    df_ingresos = finanzas.obtener_intervalo_ingresos_por_meses(año)
    df_gastos = finanzas.obtener_intervalo_gastos_por_meses(año)

    df_final = pd.merge(df_ingresos, df_gastos, on='mes', suffixes=('_ingresos', '_gastos'))
    df_final['diferencia'] = df_final['importe_ingresos'] + df_final['importe_gastos']

    df_final['tasa_ahorro'] = (df_final['diferencia'] / df_final['importe_ingresos'] * 100).round(2)
    media_tasa_ahorro = df_final['tasa_ahorro'].mean()

    st.metric(label="Tasa de ahorro media mensual", value=f"{media_tasa_ahorro:.2f} %")


def obtener_historico_axa() -> None:
    """
    Obtiene la gráfica del histórico de ingresos al plan de ahorro de axa
    """
    df: pd.DataFrame = ahorros_axa.obtener_historico()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['TOTAL_APORTADO'],
            name='Aportado',
            line=dict(color='#1f77b4'),
            marker=dict(color='#1f77b4'),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['SALDO'],
            name='Saldo',
            line=dict(color="#34960d"),
            marker=dict(color='#34960d'),
            connectgaps=True,
        )
    )

    st.plotly_chart(fig, width='stretch')


def obtener_historico_fiatc() -> None:
    """
    Obtiene la gráfica del histórico de ingresos al plan de ahorro de axa
    """
    df: pd.DataFrame = ahorros_fiatc.obtener_historico()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['TOTAL_APORTADO'],
            name='Aportado',
            line=dict(color='#1f77b4'),
            marker=dict(color='#1f77b4'),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['SALDO'],
            name='Saldo',
            line=dict(color="#34960d"),
            marker=dict(color='#34960d'),
            connectgaps=True,
        )
    )

    st.plotly_chart(fig, width='stretch')


selector_año()

tab_diferencia, tab_tasa_ahorro = st.tabs(["📈 Ingresos - Gastos", "💵 Tasa Ahorro (%)"])
with tab_diferencia:
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_intervalo_ahorro_meses()
    with col3:
        obtener_total_diferencia()
        obtener_media_diferencia()
with tab_tasa_ahorro:
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_intervalo_tasa_ahorro()
    with col3:
        obtener_media_tasa_ahorro()

tab_axa, tab_fiatc = st.tabs(["🐖 Plan Ahorro: AXA" , "🐖 Plan Ahorro: FIATC"])
with tab_axa:
    st.subheader("Plan de Ahorro AXA")
    obtener_historico_axa()
with tab_fiatc:
    st.subheader("Plan de Ahorro FIATC")
    obtener_historico_fiatc()
