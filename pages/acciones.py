import asyncio
import pandas as pd
import streamlit as st

from typing import Literal
from src.interactive_broker import InteractiveBroker
from src.locale import Locale

# Obtener el idioma del contexto
locale = Locale(st.context.locale)

# Título de la página
st.title("📈 " + locale.textos["titulo_accion"])

st.write(f'Foto fija del valor de la cartera a su situación actual a día de {pd.Timestamp.now().strftime("%d/%m/%Y")}.')

st.divider()


async def obtener_datos_broker():
    conexion = InteractiveBroker()
    conectado = await conexion.conectar()
    if not conectado:
        return None, []

    datos_cartera = await conexion.obtener_cartera()

    return conexion, datos_cartera

try:
    broker, cartera = asyncio.run(obtener_datos_broker())
except Exception:
    broker, cartera = None, []

if broker is None:
    st.warning(
        "No se pudo establecer la conexión con Interactive Brokers. "
        "Comprueba que el cliente esté abierto y escuchando en 127.0.0.1:4001."
    )
    st.stop()


if cartera:
    df: pd.DataFrame = pd.DataFrame(cartera)

    def color_negativo_rojo(valor) -> None | Literal['color: #ff4b4b'] | Literal['color: #09ab3b']:
        if isinstance(valor, (int, float)):
            if valor < 0:
                return 'color: #ff4b4b'
            elif valor > 0:
                return 'color: #09ab3b'
        else:
            ''

    # Estilo dependiente de otra columna, en este caso PyG en negativo
    def estilo_mercado_por_pyg(df_completo) -> pd.DataFrame:
        # Creamos una "tabla clonada" pero vacía (llena de textos en blanco)
        df_estilos = pd.DataFrame('', index=df_completo.index, columns=df_completo.columns)

        # Aplicamos la regla: Si PyG es menor a 0, ponemos rojo en 'Valor Mercado'
        df_estilos.loc[df_completo['PyG No Realizadas'] < 0, 'Valor Mercado'] = 'color: #ff4b4b'

        # Aplicamos la regla: Si PyG es mayor a 0, ponemos verde en 'Valor Mercado'
        df_estilos.loc[df_completo['PyG No Realizadas'] > 0, 'Valor Mercado'] = 'color: #09ab3b'

        return df_estilos

    # Aplicar estilos: primero columnas que se miran a si mismas (map)
    columnas_a_colorear = ["% Liquidación Neta", "PyG No Realizadas", "% PyG No Realizadas"]
    columnas_existentes = [col for col in columnas_a_colorear if col in df.columns]
    df_estilizado = df.style.map(color_negativo_rojo, subset=columnas_existentes)
    # Luego se aplica el estilo a toda la tabla (apply con axis=None)
    df_estilizado = df_estilizado.apply(estilo_mercado_por_pyg, axis=None)

    df_estilizado = df_estilizado.format({
        "Posición": "{:.4f}",
        "Último": "{:.2f}",
        "Precio Medio": "{:.2f}",
        "Base de Coste": "{:.2f}",
        "Valor Mercado": "{:.2f}",
        "% Liquidación Neta": "{:.2f}%",
        "PyG No Realizadas": "{:,.2f}",
        "% PyG No Realizadas": "{:.2f}%",
        "PyG Realizadas": "{:.2f}"
    })

    st.dataframe(df_estilizado, use_container_width=True)
else:
    st.info("No hay cartera disponibles en la cuenta.")

if broker.ib.isConnected():
    broker.ib.disconnect()
