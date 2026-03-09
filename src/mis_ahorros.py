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
# FUNCIONES AUXILIARES CACHEADAS
# Reciben el DataFrame como parámetro
# ============================================
@st.cache_data
def _obtener_historico(_datos: pd.DataFrame) -> pd.DataFrame:
    """
    Obtiene el histórico de datos de la compañía seleccionada en un dataframe.
    """
    return _datos

# ============================================
# CLASE PRINCIPAL
# ============================================


class MisAhorros():

    def __init__(self, compañia: str) -> None:
        # Usa función cacheada en lugar de leer directamente
        self.compañia = compañia
        self.datos = cargar_datos_ahorros(compañia)

    def obtener_historico(self) -> pd.DataFrame:
        """
        Obtiene el histórico de datos de la compañía seleccionada
        en un dataframe.

        Returns:
            pd.DataFrame: DataFrame con el histórico de todos los datos
        """
        return _obtener_historico(self.datos)
