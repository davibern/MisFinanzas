import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos_ahorros(compañia: str) -> pd.DataFrame:
    """
    Carga y preprocesa los datos del archivo parquet.
    Esta función está cacheada para evitar lecturas repetitivas.

    Returns:
        pd.DataFrame: DataFrame con los datos procesados
    """
    datos = pd.read_parquet(f'data/ahorros.{compañia}.parquet')
    return datos


# ============================================
# CLASE PRINCIPAL
# ============================================


class MisAhorros():

    def __init__(self, compañia: str) -> None:
        # Usa función cacheada en lugar de leer directamente
        self.datos = cargar_datos_ahorros(compañia)
