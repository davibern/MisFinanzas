import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.locale import Locale
from src.exportar_datos import ExportarDatos
from src.config import RUTA_BOLSA_CARTERA, Color
from src.utilidades import color_positivo_negativo

# Obtener el idioma del contexto
locale = Locale(st.context.locale)

# Sincronizo por si n8n dejó nuevos ficheros CSV de IBKR
ficheros_nuevos = ExportarDatos.procesar_ficheros_ibkr_cartera()

if ficheros_nuevos > 0:
    st.toast(f"Se ha sincronizado {ficheros_nuevos} fichero(s) de IBKR de la cartera de inversión.", icon="🔄")

if not os.path.exists(RUTA_BOLSA_CARTERA):
    st.info("No hay datos de cartera disponibles todavía.")
    st.stop()

df_cartera = pd.read_parquet(RUTA_BOLSA_CARTERA)

ultima_fecha = df_cartera["fecha"].max()
df_foto_actual = df_cartera[df_cartera["fecha"] == ultima_fecha]

# Título de la página
st.title("📈 " + locale.textos["titulo_cartera"])

fecha_formateada = ultima_fecha.strftime("%d/%m/%Y")
st.write(f"Foto fija de la cartera a día **{fecha_formateada}**.")

st.divider()

total_cartera = df_foto_actual['position_value_eur'].sum()
total_invertido = df_foto_actual['cost_basis_eur'].sum()
total_plusvalia_eur = df_foto_actual["unrealized_pnl_eur"].sum()
if total_invertido > 0:
    total_plusvalia_pct = (total_plusvalia_eur / total_invertido) * 100
else:
    total_plusvalia_pct = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Valor de la Cartera",
        value=f"{total_cartera:,.2f} €"
    )

with col2:
    st.metric(
        label="Total Invertido",
        value=f"{total_invertido:,.2f} €"
    )

with col3:
    st.metric(
        label="Plusvalía no realizada",
        value=f"{total_plusvalia_eur:+,.2f} €",
        delta=f"{total_plusvalia_pct:+.2f} %"
    )

st.divider()

columnas_visibles = [
    "symbol",
    "description",
    "quantity",
    "mark_price",
    "cost_basis_price",
    "cost_basis_eur",
    "position_value_eur",
    "unrealized_pnl_eur",
    "pnl_percent",
    "percent_of_nav",
]

df_estilado = df_foto_actual[columnas_visibles].style.map(
    color_positivo_negativo,
    subset=["unrealized_pnl_eur", "pnl_percent"]
)

st.dataframe(
    df_estilado,
    hide_index=True,
    column_config={
        "symbol": st.column_config.TextColumn(
            "Instrumento",
            help="Símbolo bursátil o ticker único que identifica el activo financiero."
        ),
        "description": st.column_config.TextColumn(
            "Descripción",
            help="Nombre completo o razón social de la empresa emisora."
        ),
        "quantity": st.column_config.NumberColumn(
            "Posición",
            help="Cantidad total de títulos o acciones que mantienes actualmente en cartera.",
            format="%.4f"
        ),
        "mark_price": st.column_config.NumberColumn(
            "Último",
            help="Último precio de cotización registrado del activo en su divisa original.",
            format="%.2f"
        ),
        "cost_basis_price": st.column_config.NumberColumn(
            "Precio Medio",
            help="Coste unitario promedio de adquisición por acción en su divisa original.",
            format="%.2f"
        ),
        "cost_basis_eur": st.column_config.NumberColumn(
            "Base Coste (€)",
            help="Capital total invertido originalmente en la posición, convertido a EUR.",
            format="%.2f €"
        ),
        "position_value_eur": st.column_config.NumberColumn(
            "Valor Mercado (€)",
            help="Valoración actual de la posición (Posición x Último) convertida a EUR.",
            format="%.2f €"
        ),
        "unrealized_pnl_eur": st.column_config.NumberColumn(
            "PyG No Realizada (€)",
            help="Ganancia o pérdida latente en EUR (Valor Mercado - Base Coste).",
            format="%+.2f €"
        ),
        "pnl_percent": st.column_config.NumberColumn(
            "PyG No Realizada (%)",
            help="Rentabilidad porcentual latente sobre el capital invertido.",
            format="%+.2f %%"
        ),
        "percent_of_nav": st.column_config.NumberColumn(
            "% Cartera",
            help="Peso o ponderación que representa este activo sobre el valor total de tu cartera.",
            format="%.2f %%"
        ),
    },
)

st.divider()

# Gráfica de evolución diaria del patrimonio total de la cuenta en EUR
st.subheader("Evolución del Patrimonio Total")

df_evolucion = (
    df_cartera.groupby("fecha", as_index=False)
    .agg({
        "position_value_eur": "sum",
        "percent_of_nav": "sum"
    })
    .sort_values(by="fecha")
    .reset_index(drop=True)
)

# Incluir efectivo líquido dividiendo entre (sum(percent_of_nav) / 100)
df_evolucion["nav_factor"] = df_evolucion["percent_of_nav"] / 100.0
df_evolucion["patrimonio_total"] = df_evolucion.apply(
    lambda r: (r["position_value_eur"] / r["nav_factor"]) if r["nav_factor"] > 0 else r["position_value_eur"],
    axis=1
).round(2)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df_evolucion["fecha"],
        y=df_evolucion["patrimonio_total"],
        mode="lines+markers",
        name="Patrimonio (€)",
        line=dict(color=Color.AZUL, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(31, 119, 180, 0.1)",
        hovertemplate="<b>Fecha:</b> %{x|%d/%m/%Y}<br><b>Patrimonio:</b> %{y:,.2f} €<extra></extra>",
    )
)

fig.update_layout(
    xaxis_title="Fecha",
    yaxis_title="Valor en EUR (€)",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=30, b=20),
)

st.plotly_chart(fig, width="stretch")
