import pandas as pd


class MisFinanzas():

    def __init__(self, mes: int, año: int) -> None:
        self.datos = pd.read_parquet("data/finanzas.parquet")
        self.mes = mes
        self.año = año

    def obtener_ingresos_mes_año(self) -> float:
        """
        Obtener los ingresos totales del mes de estudio

        Returns:
            float: total de ingresos del mes
        """
        return self.datos[
            (self.datos['año'] == self.año) &
            (self.datos['mes'] == self.mes) &
            (self.datos['tipo'] == 'Ingreso')
        ]['importe'].sum()

    def obtener_gastos_mes_año(self) -> float:
        """
        Obtener los gastos totales del mes de estudio

        Returns:
            float: total de gastos del mes
        """
        return self.datos[
            (self.datos['año'] == self.año) &
            (self.datos['mes'] == self.mes) &
            (self.datos['tipo'] == 'Gasto')
        ]['importe'].sum()
