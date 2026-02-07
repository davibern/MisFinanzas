import streamlit as st
import plotly.graph_objects as go

from datetime import datetime
from src.mis_finanzas import MisFinanzas

# Título de la página
st.title("📅 Datos del Mes")
st.write("Datos financieros agrupados por mes, con gráficos y estadísticas.")
st.write("Selecciona el año y el mes para obtener los datos correspondientes, y obtendrás\
    automáticamente la comparativa con respecto al mes anterior.")
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
        años = list(range(2024, 2027))
        año_actual = datetime.now().year

        # Calculo el índice del año actual en la lista de años
        # Si el año actual no está en la lista, uso 0 para evitar errores
        try:
            indice_defecto_año = años.index(año_actual)
        except ValueError:
            indice_defecto_año = 0
        año = st.selectbox("Año", años, index=indice_defecto_año)
    with col2:
        global mes
        meses = list(range(1, 13))
        mes_actual = datetime.now().month - 1 if datetime.now().month > 1 else 12

        # Calculo el índice del mes actual en la lista de meses
        # Si el mes actual no está en la lista, uso 0 para evitar errores
        try:
            indice_defecto_mes = meses.index(mes_actual)
        except ValueError:
            indice_defecto_mes = 0
        mes = st.selectbox("Mes", meses, index=indice_defecto_mes)
    st.markdown("---")


def obtener_resumen_mes() -> None:
    """Obtiene el resumen estadístico del mes actual y anterior y lo muestra en tarjetas."""
    st.subheader("Resumen Estadístico")
    # Obtener ingresos del mes actual y anterior y el ratio de diferencia
    ingresos: float = datos.obtener_ingresos_mes_año(año, mes)
    delta_ingresos: float = datos.obtener_ingresos_mes_año(año, mes - 1) if mes > 1 else datos.obtener_ingresos_mes_año(año - 1, 12)
    ratio_delta_ingresos: float = ((ingresos - delta_ingresos) / delta_ingresos) * 100 if delta_ingresos != 0 else 0

    # Obtener gastos del mes actual y anterior y el ratio de diferencia
    gastos: float = datos.obtener_gastos_mes_año(año, mes)
    delta_gastos: float = datos.obtener_gastos_mes_año(año, mes - 1) if mes > 1 else datos.obtener_gastos_mes_año(año - 1, 12)
    ratio_delta_gastos: float = ((gastos - delta_gastos) / delta_gastos) * 100 if delta_gastos != 0 else 0

    # Obtener balance del mes actual y anterior y el ratio de diferencia
    balance: float = ingresos + gastos
    delta_balance: float = delta_ingresos + delta_gastos
    ratio_delta_balance: float = ((balance - delta_balance) / delta_balance) * 100 if delta_balance != 0 else 0

    # Mostrar tarjetas en columnas de 3
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ingresos", ingresos, delta=f"{ratio_delta_ingresos:.2f}%",
                  help="Ingresos del mes y su diferencia con el mes anterior en porcentaje",
                  label_visibility="visible", format="euro")
    with col2:
        st.metric("Gastos", gastos, delta=f"{ratio_delta_gastos:.2f}%", delta_color="inverse",
                  help="Gastos del mes y su diferencia con el mes anterior en porcentaje",
                  label_visibility="visible", format="euro")
    with col3:
        st.metric("Balance", balance, delta=f"{ratio_delta_balance:.2f}%",
                  help="Balance del mes y su diferencia con el mes anterior en porcentaje",
                  label_visibility="visible", format="euro")


def obtener_gastos_mes() -> None:
    """Obtiene los gastos por categoría del mes actual y lo muestra en un gráfico de barras."""

    # Subtítulo para los gastos por categoría
    st.subheader("Gastos por categoría")

    # Obtener datos del mes y almacenarlos en un dataframe
    df_gastos = datos.obtener_gastos_agrupados_mes_año(año, mes)
    df_gastos['importe'] = df_gastos['importe'].abs()

    # Crear gráfico de barras con Plotly para tener control sobre la rotación de etiquetas
    fig = go.Figure(data=[
        go.Bar(
            x=df_gastos['categoria'],
            y=df_gastos['importe'],
            marker=dict(
                color=df_gastos.index,  # Color por categoría
                colorscale='Viridis'
            )
        )
    ])

    # Configurar el layout con etiquetas rotadas a 45 grados
    fig.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Importe (€)",
        height=600,
        xaxis=dict(
            tickangle=-45,  # Rotar etiquetas a 45 grados
            tickmode='linear'
        ),
        showlegend=False
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, width='stretch')


def obtener_ingresos_mes() -> None:
    """Obtiene los ingresos por categoría del mes actual y lo muestra en un gráfico de barras."""

    # Subtítulo para los gastos por categoría
    st.subheader("Ingresos por categoría")

    # Obtener datos del mes y almacenarlos en un dataframe
    df_ingresos = datos.obtener_ingresos_agrupados_mes_año(año, mes)
    df_ingresos['importe'] = df_ingresos['importe'].abs()

    # Crear gráfico de barras con Plotly para tener control sobre la rotación de etiquetas
    fig = go.Figure(data=[
        go.Bar(
            x=df_ingresos['categoria'],
            y=df_ingresos['importe'],
            marker=dict(
                color=df_ingresos.index,  # Color por categoría
                colorscale='Viridis'
            )
        )
    ])

    # Configurar el layout con etiquetas rotadas a 45 grados
    fig.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Importe (€)",
        height=600,
        xaxis=dict(
            tickangle=-45,  # Rotar etiquetas a 45 grados
            tickmode='linear'
        ),
        showlegend=False
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, width='stretch')


def obtener_detalles_mes() -> None:
    """
    Obtiene el listado del mes (se visualiza el dataframe)
    """
    st.dataframe(datos.datos.query("año == @año and mes == @mes").sort_values(by="fecha", ascending=True).reset_index(drop=True))


selector_año_mes()
obtener_resumen_mes()

tab_gastos, tab_ingresos, tab_listado = st.tabs(["🛍️ Gastos", "🪙 Ingresos", "🗒️ Listado"], default="🛍️ Gastos")

with tab_gastos:
    obtener_gastos_mes()
with tab_ingresos:
    obtener_ingresos_mes()
with tab_listado:
    obtener_detalles_mes()
