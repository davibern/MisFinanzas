import pandas as pd
import re

from pathlib import Path


class CargarCarteraIBKR:
    """
    Clase para cargar los datos de cartera en formato CSV de cartera/posiciones diarias: ibkr_cartera_operaciones_YYYYMMDD.csv
    """

    MAPEO_COLUMNAS: dict[str, str] = {
        "Symbol": "symbol",
        "Description": "description",
        "CurrencyPrimary": "currency",
        "Quantity": "quantity",
        "MarkPrice": "mark_price",
        "CostBasisPrice": "cost_basis_price",
        "CostBasisMoney": "cost_basis_money",
        "PositionValue": "position_value",
        "FifoPnlUnrealized": "fifo_pnl_unrealized",
        "FXRateToBase": "fx_rate_to_base",
        "PercentOfNAV": "percent_of_nav",
    }

    COLUMNAS_NUMERICAS: list[str] = [
        "quantity",
        "mark_price",
        "cost_basis_price",
        "cost_basis_money",
        "position_value",
        "fifo_pnl_unrealized",
        "fx_rate_to_base",
        "percent_of_nav",
    ]

    ESQUEMA_COLUMNAS: list[str] = [
        "fecha", "symbol", "description", "currency", "quantity",
        "mark_price", "cost_basis_price", "cost_basis_money",
        "position_value", "fifo_pnl_unrealized", "fx_rate_to_base",
        "cost_basis_eur", "position_value_eur", "unrealized_pnl_eur",
        "pnl_percent", "percent_of_nav", "año"
    ]

    def __init__(self, fichero: str) -> None:
        self.fichero = fichero
        self.df: pd.DataFrame = None
        self.fecha: str | None = self.extraer_fecha_fichero()

    def leer_fichero(self) -> pd.DataFrame:
        """Lee el fichero CSV de IBKR y lo almacena en self.df

        Returns:
            pd.DataFrame: Dataframe con los datos del fichero cargado
        """
        self.df = pd.read_csv(self.fichero)

        return self.df

    def limpiar_datos(self) -> pd.DataFrame:
        """Limpia y renombre todos los campos del fichero para adaptarlos a la base de datos

        Returns:
            pd.DataFrame: estructura limpia procedente del CSV
        """
        if self.df is None:
            self.leer_fichero()

        if not self.fecha:
            raise ValueError(f'No se pudo extraer la fecha (YYYYMMDD) del fichero: {self.fichero}')

        # Mapeo de columnas en estándar Python
        self.df = self.df.rename(columns=self.MAPEO_COLUMNAS)

        # Convertir a números los campos que lo sean
        for col in self.COLUMNAS_NUMERICAS:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").fillna(0.0)

        # Eliminar espacios sobrantes
        for col in ['symbol', 'description', 'currency']:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()

        # Añadir la fecha del fichero a la estructura de datos
        self.df['fecha'] = pd.to_datetime(self.fecha, format='%Y%m%d')

        # Cálculos de valores en EUR
        self.df['cost_basis_eur'] = (self.df['cost_basis_money'] * self.df['fx_rate_to_base']).round(4)
        self.df['position_value_eur'] = (self.df['position_value'] * self.df['fx_rate_to_base']).round(4)
        self.df['unrealized_pnl_eur'] = (self.df['fifo_pnl_unrealized'] * self.df['fx_rate_to_base']).round(4)

        # Porcentaje de PyG no realizada (protección contra división por cero)
        self.df['pnl_percent'] = (
            (self.df['fifo_pnl_unrealized'] / self.df['cost_basis_money']) * 100).fillna(0.0).replace([float('inf'), float('-inf')], 0.0).round(4)

        # Año para la partición del parquet
        self.df['año'] = self.df['fecha'].dt.year.astype(int)

        # Columnas ordenadas siempre por el mismo criterio
        self.df = self.df[self.ESQUEMA_COLUMNAS]

        return self.df

    def extraer_fecha_fichero(self) -> str | None:
        """Busca la fecha en el nombre del fichero

        Returns:
            str | None: fecha del fichero con la cartera en formato YYYYMMDD
        """
        nombre = Path(self.fichero).name if isinstance(self.fichero, (str, Path)) else getattr(self.fichero, 'name', '')
        coincidencia = re.search(r"(\d{8})", nombre)

        return coincidencia.group(1) if coincidencia else None
