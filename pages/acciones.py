import asyncio
import streamlit as st

from src.interactive_broker import InteractiveBroker
from src.locale import Locale

# Obtener el idioma del contexto
locale = Locale(st.context.locale)

# Título de la página
st.title("📈 " + locale.textos["titulo_accion"])


async def conectar() -> InteractiveBroker | None:
    conexion = InteractiveBroker()
    conectado = await conexion.conectar()
    if not conectado:
        return None
    return conexion


async def obtener_valores() -> list:
    return await broker.obtener_valores_cuenta()


async def obtener_cartera() -> list:
    return await broker.obtener_cartera()

try:
    broker = asyncio.run(conectar())
except RuntimeError:
    broker = None

if broker is None:
    st.warning(
        "No se pudo establecer la conexión con Interactive Brokers. "
        "Comprueba que el cliente esté abierto y escuchando en 127.0.0.1:4001."
    )
    st.stop()

st.success("Conexión establecida correctamente.")

try:
    cartera = asyncio.run(obtener_cartera())
except Exception:
    cartera = []

if cartera:
    st.dataframe(cartera)
else:
    st.info("No hay cartera disponibles en la cuenta.")

if broker.ib.isConnected():
    broker.ib.disconnect()
