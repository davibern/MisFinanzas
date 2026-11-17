import os
import streamlit as st
import pandas as pd

from src.locale import Locale
from src.exportar_datos import ExportarDatos
from src.config import RUTA_BOLSA_CARTERA
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
        "symbol": st.column_config.TextColumn("Instrumento"),
        "description": st.column_config.TextColumn("Descripción"),
        "quantity": st.column_config.NumberColumn("Posición", format="%.4f"),
        "mark_price": st.column_config.NumberColumn("Último", format="%.2f"),
        "cost_basis_price": st.column_config.NumberColumn("Precio Medio", format="%.2f"),
        "cost_basis_eur": st.column_config.NumberColumn("Base Coste (€)", format="%.2f €"),
        "position_value_eur": st.column_config.NumberColumn("Valor Mercado (€)", format="%.2f €"),
        "unrealized_pnl_eur": st.column_config.NumberColumn("PyG No Realizada (€)", format="%+.2f €"),
        "pnl_percent": st.column_config.NumberColumn("PyG No Realizada (%)", format="%+.2f %%"),
        "percent_of_nav": st.column_config.NumberColumn("% Cartera", format="%.2f %%"),
    },
)

st.divider()

st.markdown("""
### Descripciones
- **Instrumento**: Símbolo bursátil o _ticker_ único que identifica el activo financiero en el mercado donde cotiza.
- **Descripción**: Nombre completo o razón social de la empresa emisora del activo.
- **Posición**: Cantidad total de títulos o acciones (incluyendo fracciones) que mantienes actualmente en cartera.
- **Último**: Último precio de cotización registrado del activo, expresado en su divisa original de mercado.
- **Precio Medio**: Coste unitario promedio de la adquisición por acción en su divisa original, incluyendo el
  **prorrateo de las comisiones de compra.
- **Base Coste (€)**: Capital total invertido originalmente en la posición (precio de compra más comisiones),
  **convertido a tu divisa base (EUR).
- **Valor Mercado (€)**: Valoración actual de la posición (`Posición x Último`), convertida al tipo de cambio
  **vigente a tu divisa base (EUR).
- **PyG No Realizada (€)**: Ganancia o pérdida latente en EUR (`Valor Mercado - Base Coste`). Incluye tanto
  **la variación del precio como el efecto del tipo de cambio (FX).
- **PyG No Realizad (%)**: Rentabilidad porcentual latente sobre el capital invertido (`PyG No Realizada / Base Coste`).
  **en tu divisa base.
- **% Cartera**: Peso o ponderación que representa el valor de mercado de este activo respecto al valor total de toda tu cartera.
""")