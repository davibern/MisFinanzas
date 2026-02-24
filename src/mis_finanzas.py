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
    """Calcula el total de ingresos para un mes específico (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Ingreso')
    ]['importe'].sum()


@st.cache_data
def _calcular_gastos_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> float:
    """Calcula el total de gastos para un mes específico (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Gasto')
    ]['importe'].sum()


@st.cache_data
def _calcular_media_gastos_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> float:
    """Calcula la media de gasto diario para un mes, omitiendo días sin registros (función cacheada)."""

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
    """Calcula el total de gastos en un intervalo de meses (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Gasto')
    ]['importe'].sum()


@st.cache_data
def _calcular_intervalo_ingresos(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> float:
    """Calcula el total de ingresos en un intervalo de meses (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Ingreso')
    ]['importe'].sum()


@st.cache_data
def _calcular_gastos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> pd.DataFrame:
    """Agrupa los gastos por categoría para un mes específico (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('categoria')['importe'].sum().reset_index()


@st.cache_data
def _calcular_intervalo_gastos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
    """Agrupa los gastos por categoría en un intervalo de meses (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('categoria')['importe'].sum().reset_index()

@st.cache_data
def _calcular_ingresos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes: int) -> pd.DataFrame:
    """Agrupa los ingresos por categoría para un mes específico (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] == mes) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('categoria')['importe'].sum().reset_index()

@st.cache_data
def _calcular_intervalo_ingresos_agrupados_mes_año(_datos: pd.DataFrame, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
    """Agrupa los ingresos por categoría en un intervalo de meses (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['mes'] >= mes_inicio) &
        (_datos['mes'] <= mes_fin) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('categoria')['importe'].sum().reset_index()


@st.cache_data
def _calcular_intervalo_gastos_por_meses(_datos: pd.DataFrame, año: int) -> pd.DataFrame:
    """Agrupa los gastos por mes para un año completo (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['tipo'] == 'Gasto')
    ].groupby('mes')['importe'].sum().reset_index()

@st.cache_data
def _calcular_intervalo_ingresos_por_meses(_datos: pd.DataFrame, año: int) -> pd.DataFrame:
    """Agrupa los ingresos por mes para un año completo (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['tipo'] == 'Ingreso')
    ].groupby('mes')['importe'].sum().reset_index()

@st.cache_data
def _calcular_ahorro_jubilacion_por_meses(_datos: pd.DataFrame, año: int) -> pd.DataFrame:
    """Agrupa el ahorro por mes y concepto para un año completo (función cacheada)."""
    return _datos[
        (_datos['año'] == año) &
        (_datos['tipo'] == 'Gasto') &
        (_datos['categoria'] == 'Planes de pensión y previsión')
    ].groupby(['mes', 'concepto'])['importe'].sum().abs().reset_index()

# ============================================
# CLASE PRINCIPAL
# ============================================

class MisFinanzas():

    def __init__(self) -> None:
        # Usa función cacheada en lugar de leer directamente
        self.datos = cargar_datos_finanzas()

    def obtener_ingresos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtiene el total de ingresos de un mes específico.

        Args:
            año: Año a consultar
            mes: Mes a consultar (1-12)
        
        Returns:
            Total de ingresos del mes en euros
        """
        return _calcular_ingresos_mes_año(self.datos, año, mes)

    def obtener_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtiene el total de gastos de un mes específico.

        Args:
            año: Año a consultar
            mes: Mes a consultar (1-12)
        
        Returns:
            Total de gastos del mes en euros (valor negativo)
        """
        return _calcular_gastos_mes_año(self.datos, año, mes)

    def obtener_media_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Calcula la media de gasto diario de un mes, considerando solo los días con gastos registrados.

        Args:
            año: Año a consultar
            mes: Mes a consultar (1-12)
        
        Returns:
            Media de gasto diario en euros
        """
        return _calcular_media_gastos_mes_año(self.datos, año, mes)

    def obtener_intervalo_gastos(self, año: int, mes_inicio: int, mes_fin: int) -> float:
        """
        Obtiene el total de gastos en un rango de meses.

        Args:
            año: Año a consultar
            mes_inicio: Mes inicial del intervalo (1-12)
            mes_fin: Mes final del intervalo (1-12)

        Returns:
            Total de gastos del periodo en euros (valor negativo)
        """
        return _calcular_intervalo_gastos(self.datos, año, mes_inicio, mes_fin)

    def obtener_intervalo_ingresos(self, año: int, mes_inicio: int, mes_fin: int) -> float:
        """
        Obtiene el total de ingresos en un rango de meses.

        Args:
            año: Año a consultar
            mes_inicio: Mes inicial del intervalo (1-12)
            mes_fin: Mes final del intervalo (1-12)

        Returns:
            Total de ingresos del periodo en euros
        """
        return _calcular_intervalo_ingresos(self.datos, año, mes_inicio, mes_fin)

    def obtener_gastos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtiene los gastos de un mes agrupados por categoría.

        Args:
            año: Año a consultar
            mes: Mes a consultar (1-12)

        Returns:
            DataFrame con columnas ['categoria', 'importe']
        """
        return _calcular_gastos_agrupados_mes_año(self.datos, año, mes)

    def obtener_intervalo_gastos_agrupados_mes_año(self, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
        """
        Obtiene los gastos de un rango de meses agrupados por categoría.

        Args:
            año: Año a consultar
            mes_inicio: Mes inicial del intervalo (1-12)
            mes_fin: Mes final del intervalo (1-12)

        Returns:
            DataFrame con columnas ['categoria', 'importe']
        """
        return _calcular_intervalo_gastos_agrupados_mes_año(self.datos, año, mes_inicio, mes_fin)

    def obtener_ingresos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtiene los ingresos de un mes agrupados por categoría.

        Args:
            año: Año a consultar
            mes: Mes a consultar (1-12)

        Returns:
            DataFrame con columnas ['categoria', 'importe']
        """
        return _calcular_ingresos_agrupados_mes_año(self.datos, año, mes)

    def obtener_intervalo_ingresos_agrupados_mes_año(self, año: int, mes_inicio: int, mes_fin: int) -> pd.DataFrame:
        """
        Obtiene los ingresos de un rango de meses agrupados por categoría.

        Args:
            año: Año a consultar
            mes_inicio: Mes inicial del intervalo (1-12)
            mes_fin: Mes final del intervalo (1-12)

        Returns:
            DataFrame con columnas ['categoria', 'importe']
        """
        return _calcular_intervalo_ingresos_agrupados_mes_año(self.datos, año, mes_inicio, mes_fin)

    def obtener_intervalo_gastos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtiene los gastos totales de cada mes de un año.

        Args:
            año: Año a consultar

        Returns:
            DataFrame con columnas ['mes', 'importe'] para los 12 meses
        """
        return _calcular_intervalo_gastos_por_meses(self.datos, año)

    def obtener_intervalo_ingresos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtiene los ingresos totales de cada mes de un año.

        Args:
            año: Año a consultar

        Returns:
            DataFrame con columnas ['mes', 'importe'] para los 12 meses
        """
        return _calcular_intervalo_ingresos_por_meses(self.datos, año)
    
    def obtener_ahorro_jubilacion_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtiene el ahorro por mes para un año completo.

        Args:
            año: Año a consultar

        Returns:
            DataFrame con columnas ['mes', 'importe'] para los 12 meses
        """
        return _calcular_ahorro_jubilacion_por_meses(self.datos, año)   
