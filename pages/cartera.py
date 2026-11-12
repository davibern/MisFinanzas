import os
import streamlit as st
import pandas as pd

from src.locale import Locale
from src.exportar_datos import ExportarDatos
from src.config import RUTA_BOLSA_CARTERA

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
    "cost_basis_eur",
    "position_value_eur",
    "unrealized_pnl_eur",
    "pnl_percent",
    "percent_of_nav",
]

st.dataframe(
    df_foto_actual[columnas_visibles],
    hide_index=True,
    column_config={
        "position_value_eur": st.column_config.NumberColumn("Valor (€)", format="%.2f €"),
        "cost_basis_eur": st.column_config.NumberColumn("Coste (€)", format="%.2f €"),
        "unrealized_pnl_eur": st.column_config.NumberColumn("PyG (€)", format="%.2f €"),
        "pnl_percent": st.column_config.NumberColumn("PyG (%)", format="%.2f %%"),
        "percent_of_nav": st.column_config.NumberColumn("% Cartera", format="%.2f %%"),
    },
)
