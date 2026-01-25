import pandas as pd


class MisFinanzas():

    def __init__(self) -> None:
        self.datos = pd.read_parquet("data/finanzas.parquet")
        # Convertir columnas de partición de categorical a int
        self.datos['año'] = self.datos['año'].astype(int)
        self.datos['mes'] = self.datos['mes'].astype(int)

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

    def obtener_intervalo_gastos_agrupados_mes_año(self, año: int, mes: int) -> pd.DataFrame:
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
