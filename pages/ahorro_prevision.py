import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from datetime import datetime
from src.mis_finanzas import MisFinanzas
from src.mis_ahorros import MisAhorros
from src.enums import Mes
from src.config import Color
from src.locale import Locale

# Obtener el idioma del contexto
locale = Locale(st.context.locale)

# Título de la página
st.title("💰 " + locale.textos["titulo_ahorro"])
st.write(locale.textos["descripcion_ahorro_1"])
st.write(locale.textos["descripcion_ahorro_2"])

# Mapear número de mes a nombre en español
nombres_meses = Mes.get_map_dict()

# Cargar datos de finanzas y ahorros
finanzas = MisFinanzas()
ahorros_axa = MisAhorros('axa')
ahorros_fiatc = MisAhorros('fiatc')


def selector_año() -> None:
    """Selector de año y mes"""
    st.markdown("---")
    st.markdown("#### " + locale.textos["selecciona_ano_mes_consultar"])
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
        año = st.selectbox(locale.textos["opcion"]["año"], años, index=indice_defecto_año)
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
            name=locale.textos["ahorro"]
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

    st.metric(label=locale.textos["ahorro_total_ano"], value=f"{total_diferencia:.2f} €")


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
    st.metric(label=locale.textos["ahorro_medio_mensual"], value=f"{media_diferencia:.2f} €")


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
            name=locale.textos["tasa_ahorro_porcentaje"]
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

    st.metric(label=locale.textos["tasa_ahorro_media_mensual"], value=f"{media_tasa_ahorro:.2f} %")


def obtener_historico_axa() -> None:
    """
    Obtiene la gráfica del histórico de ingresos al plan de ahorro de axa
    """
    df: pd.DataFrame = ahorros_axa.obtener_historico()

    if df.empty:
        st.warning(locale.textos["error_datos_ahorro_axa"])
        return

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['TOTAL_APORTADO'],
            name=locale.textos["aportado"],
            line=dict(color=Color.AZUL),
            marker=dict(color=Color.AZUL),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['SALDO'],
            name=locale.textos["saldo"],
            line=dict(color=Color.VERDE),
            marker=dict(color=Color.VERDE),
            connectgaps=True,
        )
    )

    st.plotly_chart(fig, width='stretch')


def obtener_total_aportado_axa() -> None:
    """
    Obtiene el total aportado al plan de axa
    """
    st.metric(label=locale.textos["aportado_plan_axa"], value=f"{ahorros_axa.obtener_total_aportado_plan_ahorro():.2f} €")


def obtener_total_acumulado_axa() -> None:
    """
    Obtiene el total acumulado aportado al plan de axa
    """
    acumulado: float = ahorros_axa.obtener_total_acumulado_plan_ahorro()
    aportado: float = ahorros_axa.obtener_total_aportado_plan_ahorro()
    delta: float = ((acumulado-aportado)/aportado)*100
    st.metric(
        label=locale.textos["acumulado_plan_axa"],
        value=f"{acumulado:.2f} €",
        delta=f"{delta:.2f} %"
    )


def obtener_historico_fiatc() -> None:
    """
    Obtiene la gráfica del histórico de ingresos al plan de ahorro de fiatc
    """
    df: pd.DataFrame = ahorros_fiatc.obtener_historico()

    if df.empty:
        st.warning(locale.textos["error_datos_ahorro_fiatc"])
        return

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['TOTAL_APORTADO'],
            name=locale.textos["aportado"],
            line=dict(color=Color.AZUL),
            marker=dict(color=Color.AZUL),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df['FECHA'],
            y=df['SALDO'],
            name=locale.textos["saldo"],
            line=dict(color=Color.VERDE),
            marker=dict(color=Color.VERDE),
            connectgaps=True,
        )
    )

    st.plotly_chart(fig, width='stretch')


def obtener_total_aportado_fiatc() -> None:
    """
    Obtiene el total aportado al plan de fiatc
    """
    st.metric(
        label=locale.textos["aportado_plan_fiatc"],
        value=f"{ahorros_fiatc.obtener_total_aportado_plan_ahorro():.2f} €",
    )


def obtener_total_acumulado_fiatc() -> None:
    """
    Obtiene el total acumulado aportado al plan de fiatc
    """
    acumulado: float = ahorros_fiatc.obtener_total_acumulado_plan_ahorro()
    aportado: float = ahorros_fiatc.obtener_total_aportado_plan_ahorro()
    delta: float = ((acumulado-aportado)/aportado)*100
    st.metric(
        label=locale.textos["acumulado_plan_fiatc"],
        value=f"{acumulado:.2f} €",
        delta=f"{delta:.2f} %"
    )


selector_año()

tab_diferencia, tab_tasa_ahorro = st.tabs([locale.textos["tabs_ahorro_prevision"]["ingresos_gastos"], locale.textos["tabs_ahorro_prevision"]["tasa_ahorro"]])
with tab_diferencia:
    st.write(locale.textos["info_diferencia_1"])
    st.write(locale.textos["info_diferencia_2"])
    st.write(locale.textos["info_diferencia_3"])
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_intervalo_ahorro_meses()
    with col3:
        obtener_total_diferencia()
        obtener_media_diferencia()
with tab_tasa_ahorro:
    st.write(locale.textos["info_tasa_ahorro_1"])
    st.write(locale.textos["info_tasa_ahorro_2"])
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_intervalo_tasa_ahorro()
    with col3:
        obtener_media_tasa_ahorro()

tab_axa, tab_fiatc = st.tabs([locale.textos["tabs_ahorro_prevision"]["plan_axa"], locale.textos["tabs_ahorro_prevision"]["plan_fiatc"]])
with tab_axa:
    st.subheader(locale.textos["plan_ahorro_axa"])
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_historico_axa()
    with col3:
        obtener_total_aportado_axa()
        obtener_total_acumulado_axa()
with tab_fiatc:
    st.subheader(locale.textos["plan_ahorro_fiatc"])
    col1, col2, col3 = st.columns([2.5, 0.5, 1], vertical_alignment='center')
    with col1:
        obtener_historico_fiatc()
    with col3:
        obtener_total_aportado_fiatc()
        obtener_total_acumulado_fiatc()
