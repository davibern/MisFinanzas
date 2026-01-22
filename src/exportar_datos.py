import pandas as pd
from src.cargar_fichero import CargarFichero


class ExportarDatos:
    def __init__(self, datos: CargarFichero):
        self.datos = datos

    def validar_año_mes(self) -> bool:
        """
        Valida que el año y el mes ya hayan sido procesados previamente para no volverlos a procesar

        Returns:
            bool: True si el año y el mes ya han sido procesados, False en caso contrario
        """
        try:
            df_existente = pd.read_parquet("data/finanzas.parquet")
        except FileNotFoundError:
            return False

        # Obtengo los pares únicos del año y mes en los nuevos
        nuevos_periodos = self.datos.df[['año', 'mes']].drop_duplicates()

        # Objeto los meses y años actuales del fichero original
        periodos_existentes = df_existente[['año', 'mes']].drop_duplicates()

        # Paso a set para trabajar de forma eficiente
        set_existente = set(map(tuple, periodos_existentes.values))
        set_nuevos = set(map(tuple, nuevos_periodos.values))

        # Compruebo si hay pares nuevos
        return set_nuevos.issubset(set_existente)

    def exportar(self):
        """
        Exporta los datos a un fichero parquet
        """
        if self.validar_año_mes():
            print("El año y el mes ya han sido procesados")
        else:
            self.datos.df.to_parquet(
                "data/finanzas.parquet",
                engine="pyarrow",
                compression="snappy",
                partition_cols=["año", "mes"],
                index=False,
            )
