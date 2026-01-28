import streamlit as st
import plotly.graph_objects as go

from src.mis_finanzas import MisFinanzas

# Título de la página
st.title("📅 Datos del Mes")

# Subtítulo para los gastos por categoría
st.subheader("Gastos por categoría")

# Cargar datos
datos = MisFinanzas()

# Obtener datos del mes y almacenarlos en un dataframe
df_gastos = datos.obtener_gastos_agrupados_mes_año(2025, 12)
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