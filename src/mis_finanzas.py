import pandas as pd


class MisFinanzas():

    def __init__(self, df: pd.DataFrame, mes: int, año: int) -> None:
        self.df = df
        self.mes = mes
        self.año = año

    def obtener_ingresos_mes_año(self) -> float:
        """
        Obtener los ingresos totales del mes de estudio

        Returns:
            float: total de ingresos del mes
        """
        filters = [
            ("año", "==", self.año),
            ("mes", "==", self.mes),
            ("tipo", "==", "Ingreso")
        ]
        return pd.read_parquet(
            "data/finanzas.parquet", filters=filters
        )['importe'].sum()

    def obtener_gastos_mes_año(self) -> float:
        """
        Obtener los gastos totales del mes de estudio

        Returns:
            float: total de gastos del mes
        """
        filters = [
            ("año", "==", self.año),
            ("mes", "==", self.mes),
            ("tipo", "==", "Gasto")
        ]
        return pd.read_parquet(
            "data/finanzas.parquet", filters=filters
        )['importe'].sum()
