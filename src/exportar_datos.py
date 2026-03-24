import pandas as pd
import os
import shutil

from src.cargar_datos_bancarios import CargarFicheroBancario
from src.cargar_datos_ahorros import CargarFicheroAhorro
from src.config import RUTA_FINANZAS_PARQUET


class ExportarDatos:
    def __init__(self, datos: CargarFicheroBancario | CargarFicheroAhorro, tipo: str, compañia: str | None = None) -> None:
        self.datos = datos
        self.tipo = tipo
        self.compañia = compañia

    def validar_año_mes(self) -> bool:
        """
        Valida que el año y el mes ya hayan sido procesados previamente para no volverlos a procesar

        Returns:
            bool: True si el año y el mes ya han sido procesados, False en caso contrario
        """
        try:
            df_existente = pd.read_parquet(RUTA_FINANZAS_PARQUET)
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

    def exportar_parquet(self) -> int:
        """
        Exporta los datos a un fichero parquet.

        Dependiendo del tipo de datos, se guardarán en uno u otro directorio.
        """
        # Aseguramos que el directorio principal de datos existe
        os.makedirs("data", exist_ok=True)

        if self.tipo == 'bancario':
            if self.validar_año_mes():
                return 0
            else:
                self.datos.df.to_parquet(
                    RUTA_FINANZAS_PARQUET,
                    engine="pyarrow",
                    compression="snappy",
                    partition_cols=["año", "mes"],
                    index=False,
                )
                return 1
        elif self.tipo == 'ahorro':
            # Borrar si ya existe para asegurar sobreescribir totalmente
            archivo = f"data/ahorros.{self.compañia}.parquet"
            if os.path.exists(archivo):
                if os.path.isdir(archivo):
                    shutil.rmtree(archivo)
                else:
                    os.remove(archivo)
            # Generar el parquet
            self.datos.df.to_parquet(
                archivo,
                engine="pyarrow",
                compression="snappy",
                index=False,
            )
        else:
            raise ValueError('Tipo de datos no reconocido. Debe ser de tipo "bancario" o "ahorro".')
