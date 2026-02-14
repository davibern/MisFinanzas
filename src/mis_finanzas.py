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


class MisFinanzas():

    def __init__(self) -> None:
        # Usa función cacheada en lugar de leer directamente
        self.datos = cargar_datos_finanzas()

    def obtener_ingresos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener los ingresos totales del mes de estudio

        Returns:
            float: total de ingresos del mes
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] == mes) &
            (self.datos['tipo'] == 'Ingreso')
        ]['importe'].sum()

    def obtener_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener los gastos totales del mes de estudio

        Returns:
            float: total de gastos del mes
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] == mes) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe'].sum()

    def obtener_media_gastos_mes_año(self, año: int, mes: int) -> float:
        """
        Obtener la media del gasto diario sumando los gastos por día y calculando la media de esos totales (omitiendo días sin registros)
        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio
        Return:
            float: media del gasto diario del mes
        """

        # Filtrar los gastos del mes y año correspondientes
        gastos_mes: pd.DataFrame = self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] == mes) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe']

        # Si no hay gastos ese mes, evitamos errores devolviendo 0.0
        if gastos_mes.empty:
            return 0.0

        # Agrupar por fecha y sumar los gastos de cada día, se usa abs() para convertir los gastos a positivos
        gastos_diarios = gastos_mes.groupby(self.datos['fecha']).sum().abs()

        # Calcular la media de los gastos diarios
        return gastos_diarios.mean()

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
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] >= mes_inicio) &
            (self.datos['mes'] <= mes_fin) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe'].sum()

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
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] >= mes_inicio) &
            (self.datos['mes'] <= mes_fin) &
            (self.datos['tipo'] == 'Ingreso')
        ]['importe'].sum()

    def obtener_gastos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtener los gastos de un mes y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos agrupados por categoría
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] == mes) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe'].groupby(self.datos['categoria']).sum().reset_index()

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
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] >= mes_inicio) &
            (self.datos['mes'] <= mes_fin) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe'].groupby(self.datos['categoria']).sum().reset_index()

    def obtener_ingresos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
        """
        Obtener los ingresos de un mes y año agrupados por categoría

        Args:
            año (int): el año de estudio
            mes (int): el mes de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos agrupados por categoría
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] == mes) &
            (self.datos['tipo'] == 'Ingreso')
        ]['importe'].groupby(self.datos['categoria']).sum().reset_index()

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
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['mes'] >= mes_inicio) &
            (self.datos['mes'] <= mes_fin) &
            (self.datos['tipo'] == 'Ingreso')
        ]['importe'].groupby(self.datos['categoria']).sum().reset_index()

    def obtener_intervalo_gastos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtener la suma de los gastos por meses en un intervalo de 12 meses

        Args:
            año (int): el año de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de gastos por mes
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['tipo'] == 'Gasto')
        ].groupby(self.datos['mes'])['importe'].sum().reset_index()

    def obtener_intervalo_ingresos_por_meses(self, año: int) -> pd.DataFrame:
        """
        Obtener la suma de los ingresos por meses en un intervalo de 12 meses

        Args:
            año (int): el año de estudio

        Returns:
            pd.DataFrame: DataFrame con los datos de ingresos por mes
        """
        return self.datos[
            (self.datos['año'] == año) &
            (self.datos['tipo'] == 'Ingreso')
        ].groupby(self.datos['mes'])['importe'].sum().reset_index()
