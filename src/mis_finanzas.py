import pandas as pd
import streamlit as st


@st.cache_data
def cargar_datos_finanzas() -> pd.DataFrame:
    """
    Carga y preprocesa los datos del archivo parquet.
    Esta función está cacheada para evitar lecturas repetitivas.

    Returns:
        pd.DataFrame: DataFrame con los datos procesados
    """
    datos = pd.read_parquet("data/finanzas.parquet")
    # Convertir columnas de partición de categorical a int
    datos[['año', 'mes']] = datos[['año', 'mes']].astype(int)
    return datos


# ============================================
# FUNCIONES AUXILIARES CACHEADAS
# Reciben el DataFrame como parámetro
# ============================================
@st.cache_data
def _calcular_ingresos_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> float:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes: el mes de estudio
    
    Returns:
        float: total de ingresos del mes
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Ingreso')
    ]['importe'].sum()


@st.cache_data
def _calcular_gastos_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> float:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes: el mes de estudio
    
    Returns:
        float: total de gastos del mes
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Gasto')
    ]['importe'].sum()


@st.cache_data
def _calcular_media_gastos_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> float:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes: el mes de estudio
    
    Returns:
        float: media del gasto diario del mes
    """

    # Filtrar los gastos del mes y año correspondientes
    gastos_mes: pd.DataFrame = _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Gasto')
    ]['importe']

    # Si no hay gastos ese mes, evitamos errores devolviendo 0.0
    if gastos_mes.empty:
        return 0.0

    # Agrupar por fecha y sumar los gastos de cada día, se usa abs() para convertir los gastos a positivos
    gastos_diarios = gastos_mes.groupby(_datos['fecha']).sum().abs()

    # Calcular la media de los gastos diarios
    return gastos_diarios.mean()


@st.cache_data
def _calcular_intervalo_gastos(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> float:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes_inicio: el mes inicial
        mes_fin: el mes final
    
    Returns:
        float: total de gastos imputados en el periodo de estudio
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Gasto')
    ]['importe'].sum()


@st.cache_data
def _calcular_intervalo_ingresos(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> float:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes_inicio: el mes inicial
        mes_fin: el mes final
    
    Returns:
        float: total de ingresos imputados en el periodo de estudio
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Ingreso')
    ]['importe'].sum()


@st.cache_data
def _calcular_gastos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes: el mes de estudio
    
    Returns:
        pd.DataFrame: DataFrame con los gastos agrupados por categoría
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('categoria')['importe'].sum().reset_index()


@st.cache_data
def _calcular_intervalo_gastos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes_inicio: el mes inicial
        mes_fin: el mes final
    
    Returns:
        pd.DataFrame: DataFrame con los gastos agrupados por categoría
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('categoria')['importe'].sum().reset_index()

@st.cache_data
def _calcular_ingresos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes: el mes de estudio
    
    Returns:
        pd.DataFrame: DataFrame con los ingresos agrupados por categoría
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('categoria')['importe'].sum().reset_index()

@st.cache_data
def _calcular_intervalo_ingresos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
        mes_inicio: el mes inicial
        mes_fin: el mes final
    
    Returns:
        pd.DataFrame: DataFrame con los ingresos agrupados por categoría
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('categoria')['importe'].sum().reset_index()


@st.cache_data
def _calcular_intervalo_gastos_por_meses(_datos: pd.DataFrame, año: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
    
    Returns:
        pd.DataFrame: DataFrame con los gastos agrupados por mes
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('mes')['importe'].sum().reset_index()

@st.cache_data
def _calcular_intervalo_ingresos_por_meses(_datos: pd.DataFrame, año: int) -> pd.DataFrame:
    """
        Args:
        _datos: DataFrame con los datos financieros (el _ indica que no se usa para el hash del cache)
        año: el año de estudio
    
    Returns:
        pd.DataFrame: DataFrame con los ingresos agrupados por mes
    """
    return _datos[
        (_datos['año'] == año) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('mes')['importe'].sum().reset_index()

# ============================================
# CLASE PRINCIPAL
# ============================================

class MisFinanzas():

    def __init__(self) -> None:
        # Usa función cacheada en lugar de leer directamente
        self.datos = cargar_datos_finanzas()

    def obtener_ingresos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener los ingresos totales del año y mes de estudio

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio
        
        Returns:
            float: total de ingresos del mes
        """
        return _calcular_ingresos_mes_año(self.datos, año, mes)

    def obtener_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener los gastos totales del año y mes de estudio

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio
        
        Returns:
            float: total de gastos del mes
        """
        return _calcular_gastos_mes_año(self.datos, año, mes)

    def obtener_media_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener la media del gasto diario sumando los gastos por día y calculando la media de esos totales (omitiendo días sin registros)
        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio
        Return:
            float: media del gasto diario del mes
        """
        return _calcular_media_gastos_mes_año(self.datos, año, mes)

    def obtener_intervalo_gastos(self, año: int, mes_inicio: int, mes_fin: int) -> float:
        """
        Obtener los gastos totales en un intervalo de fecha

        Args:
            año (int): el año de estudio
            mes_inicio (int): el mes inicial
            mes_fin (int): el mes final

        Returns:
            float: total de gastos imputados en el periodo de estudio
        """
        return _calcular_intervalo_gastos(self.datos, año, mes_inicio, mes_fin)

    def obtener_intervalo_ingresos(self, año: int, mes_inicio: int, mes_fin: int) -> float:
        """
        Obtener los ingresos totales en un intervalo de fecha

        Args:
            año (int): el año de estudio
            mes_inicio (int): el mes inicial
            mes_fin (int): el mes final

        Returns:
            float: total de ingresos imputados en el periodo de estudio
        """
        return _calcular_intervalo_ingresos(self.datos, año, mes_inicio, mes_fin)

    def obtener_gastos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtener los gastos de un mes y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos agrupados por categoría
        """
        return _calcular_gastos_agrupados_mes_año(self.datos, año, mes)

    def obtener_intervalo_gastos_agrupados_mes_año(self, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
        """
        Obtener los gastos de un intervalo de meses y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes_inicio (int): el mes inicial
            mes_fin (int): el mes final
        Returns:
            pd.DataFrame: DataFrame con los datos de gastos agrupados por categoría
        """
        return _calcular_intervalo_gastos_agrupados_mes_año(self.datos, año, mes_inicio, mes_fin)

    def obtener_ingresos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtener los ingresos de un mes y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos agrupados por categoría
        """
        return _calcular_ingresos_agrupados_mes_año(self.datos, año, mes)

    def obtener_intervalo_ingresos_agrupados_mes_año(self, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
        """
        Obtener los ingresos de un intervalo de meses y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes_inicio (int): el mes inicial
            mes_fin (int): el mes final
        Returns:
            pd.DataFrame: DataFrame con los datos de ingresos agrupados por categoría
        """
        return _calcular_intervalo_ingresos_agrupados_mes_año(self.datos, año, mes_inicio, mes_fin)

    def obtener_intervalo_gastos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtener la suma de los gastos por meses en un intervalo de 12 meses

        Args:
            año (int): el año de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos por mes
        """
        return _calcular_intervalo_gastos_por_meses(self.datos, año)

    def obtener_intervalo_ingresos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtener la suma de los ingresos por meses en un intervalo de 12 meses

        Args:
            año (int): el año de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de ingresos por mes
        """
        return _calcular_intervalo_ingresos_por_meses(self.datos, año)
