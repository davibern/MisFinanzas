import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos_caja() -> pd.DataFrame:
    """
    Carga y preprocesa los datos del archivo parquet.
    Esta función está cacheada para evitar lecturas repetitivas.

    Returns:
        pd.DataFrame: DataFrame con los datos procesados
    """
    try:
        datos = pd.read_parquet(f'data/caja.parquet')
    except FileNotFoundError:
        # Si el archivo no existe, devolver un DataFrame vacío
        datos = pd.DataFrame()
    return datos


# ============================================
# CLASE PRINCIPAL
# ============================================


class MisCajas:

    def __init__(self) -> None:
        # Usar función cacheada para leer el parquet
        self.datos = cargar_datos_caja()
    
    def obtener_historico(self) -> pd.DataFrame:
        """
        Obtiene el histórico de datos de flujos de caja en un dataframe.

        Returns:
            pd.DataFrame: DataFrame con el histórico de todos los datos
        """
        return self.datos
    
    def obtener_media_caja_3_meses(self) -> float:
        """
        Obtiene la media de los últimos 3 meses de flujo de caja

        Returns:
            float: Media de los últimos 3 meses de flujo de caja
        """
        return self.datos['CAJA'].tail(3).mean()
    
    def obtener_media_caja_6_meses(self) -> float:
        """
        Obtiene la media de los últimos 6 meses de flujo de caja

        Returns:
            float: Media de los últimos 6 meses de flujo de caja
        """
        return self.datos['CAJA'].tail(6).mean()
    
    def obtener_media_caja_12_meses(self) -> float:
        """
        Obtiene la media de los últimos 12 meses de flujo de caja

        Returns:
            float: Media de los últimos 12 meses de flujo de caja
        """
        return self.datos['CAJA'].tail(12).mean()