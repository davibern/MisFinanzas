import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from datetime import datetime
from src.mis_finanzas import MisFinanzas

# Título de la página
st.title("📅 Datos del Mes")
st.write("Estadísticas financieras del mes. Podrás analizar tus ingresos, gastos y balance.")
st.write("Consulta los detalles de los gastos e ingresos y el detalle de cada movimiento individualmente.")

# Cargar datos
datos = MisFinanzas()


def selector_año_mes() -> None:
    """Selector de año y mes"""
    st.markdown("---")
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
        año = st.selectbox("Año", años, index=indice_defecto_año, help="Selecciona el año que deseas consultar")
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
        mes = st.selectbox("Mes", meses, index=indice_defecto_mes, help="Selecciona el mes que deseas consultar")
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

    # Obtener la media de gasto diario del mes actual y anterior y el ratio de diferencia
    media_gasto_diario: float = datos.obtener_media_gastos_mes_año(año, mes)
    delta_media_gasto_diario: float = datos.obtener_media_gastos_mes_año(año, mes - 1) if mes > 1 else datos.obtener_media_gastos_mes_año(año - 1, 12)
    ratio_delta_media_gasto_diario: float = ((media_gasto_diario - delta_media_gasto_diario) / delta_media_gasto_diario * 100) \
        if delta_media_gasto_diario != 0 else 0

    # Mostrar tarjetas en columnas de 4
    col1, col2, col3, col4 = st.columns(4)
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
    with col4:
        st.metric("Media de gasto diario", media_gasto_diario, delta=f"{ratio_delta_media_gasto_diario:.2f}%", delta_color="inverse",
                  help="Media de gasto diario del mes y su diferencia con el mes anterior en porcentaje",
                  label_visibility="visible", format="euro")


def obtener_gastos_mes() -> None:
    """Obtiene los gastos por categoría del mes actual y lo muestra en un gráfico de barras."""

    # Subtítulo para los gastos por categoría
    st.subheader("Gastos por categoría")

    # Obtener datos del mes y almacenarlos en un dataframe
    df_gastos = datos.obtener_gastos_agrupados_mes_año(año, mes)

    # Validar si no hay datos para salir antes de intentar graficar
    if df_gastos.empty:
        st.info("No hay datos de gastos para el mes seleccionado.")
        return

    # Convertir los importes a valores absolutos para mostrar el grafico correctamente
    df_gastos['importe'] = df_gastos['importe'].abs()

    # Crear gráfico de barras con Plotly para tener control sobre la rotación de etiquetas
    fig_hist = go.Figure(data=[
        go.Bar(
            x=df_gastos['categoria'],
            y=df_gastos['importe'],
            marker=dict(
                color=df_gastos.index,
                colorscale='Viridis'
            )
        )
    ])

    # Configurar el layout con etiquetas rotadas a 45 grados
    fig_hist.update_layout(
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
    st.plotly_chart(fig_hist, width='stretch')


def obtener_gastos_top_5_mes() -> None:
    st.subheader("Top de gastos del mes")
    col_burbuja, col_top_gasto = st.columns(2)
    with col_burbuja:
        # Control de usuario para "zoom" (tamaño máximo de burbuja)
        diametro_burbuja = st.slider("Tamaño máximo de burbuja (px)", min_value=40, max_value=200, value=180)
    with col_top_gasto:
        # Control para el top de gastos
        control_tope_gasto = st.slider("Filtra el tope de gastos máximos (3 ó 5)", min_value=3, max_value=5, value=4)

    # Obtener y validar datos
    df_gastos = datos.obtener_gastos_agrupados_mes_año(año, mes)
    if df_gastos.empty:
        st.info("No hay datos de gastos para el mes seleccionado.")
        return

    # Asegurar que 'importe' sea numérico, sin NaN y en valor absoluto
    df_gastos['importe'] = pd.to_numeric(df_gastos.get('importe', pd.Series()), errors='coerce').fillna(0).abs()

    # Mostrar solo el top 5 de gastos por cuantía
    df_gastos = df_gastos.sort_values(by='importe', ascending=False).head(control_tope_gasto)
    if df_gastos.empty:
        st.info("No hay gastos para mostrar en el Top 5.")
        return

    # Preparar tamaños como lista de floats (Plotly valida mejor listas simples)
    diametros = df_gastos['importe'].astype(float).tolist()
    max_importe = max(diametros) if diametros else 0
    # Tamaño de la burbuja
    diametro_ref = 2. * max_importe / (diametro_burbuja ** 2) if max_importe > 0 else 1

    # Usar posiciones numéricas en X para reducir la distancia entre categorías
    categorias = df_gastos['categoria'].astype(str).tolist()
    x_pos = list(range(len(categorias)))

    fig_bub = go.Figure(data=[
        go.Scatter(
            x=x_pos,
            y=df_gastos['importe'].tolist(),
            mode='markers',
            marker=dict(
                size=diametros,
                sizemode='area',
                sizeref=diametro_ref,
                sizemin=6,
                color=diametros,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=10, color='rgba(0,0,0,0.2)')
            ),
            hovertemplate='%{text}<br>Importe: €%{y:.2f}<extra></extra>',
            text=categorias
        )
    ])

    fig_bub.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Importe (€)",
        height=500,
        xaxis=dict(
            tickmode='array',
            tickvals=x_pos,
            ticktext=categorias,
            tickangle=-45,
            range=[-0.6, len(categorias) - 0.4]
        ),
        margin=dict(l=40, r=40, t=40, b=120),
        showlegend=False
    )

    st.plotly_chart(fig_bub, width='stretch')


def obtener_ingresos_mes() -> None:
    """Obtiene los ingresos por categoría del mes actual y lo muestra en un gráfico de barras."""

    # Subtítulo para los gastos por categoría
    st.subheader("Ingresos por categoría")

    # Obtener datos del mes y almacenarlos en un dataframe
    df_ingresos = datos.obtener_ingresos_agrupados_mes_año(año, mes)

    # Validar si no hay datos para salir antes de intentar graficar
    if df_ingresos.empty:
        st.info("No hay datos de ingresos para el mes seleccionado.")
        return

    # Convertir los importes a valores absolutos para mostrar el grafico correctamente
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
    obtener_gastos_top_5_mes()
with tab_ingresos:
    obtener_ingresos_mes()
with tab_listado:
    obtener_detalles_mes()
