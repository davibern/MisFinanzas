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
    try:
        datos = pd.read_parquet(f'data/ahorros.{compañia.lower()}.parquet')
    except FileNotFoundError:
        # Si el archivo no existe, devolver un DataFrame vacío
        datos = pd.DataFrame()
    return datos


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
        return self.datos

    def obtener_total_aportado_plan_ahorro(self) -> float:
        """
        Obtiene el total aportado al plan de ahorros

        Returns:
            float: Suma de las cantidades aportada al plan de ahorro
        """
        return self.datos['IMPORTE'].sum()

    def obtener_total_acumulado_plan_ahorro(self) -> float:
        """
        Obtiene el último dato almacenado como acumulado del plan

        Returns:
            float: Último dato almacenado en el dataframe que devuelve el total acumulado
        """
        return self.datos['SALDO'].dropna().iloc[-1]
