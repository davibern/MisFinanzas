import pandas as pd


class CargarFicheroCaja:
    def __init__(self, file) -> None:
        self.file = file
        self.df: pd.DataFrame = None

    def limpiar_datos(self) -> pd.DataFrame:
        """
        Limpia y procesa los datos y los guarda en self.df
        """
        # 1. Carga inicial al atributo de clase
        self.df = pd.read_csv(self.file)

        # 2. Limpieza de columnas numéricas
        for col in ['CAJA']:
            self.df[col] = (
                self.df[col].astype(str)
                .str.replace('€', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.strip()
            )
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # 3. Procesar Fechas
        self.df['FECHA'] = pd.to_datetime(self.df['FECHA'], dayfirst=True, errors='coerce')
        self.df['FECHA'] = self.df['FECHA'].ffill()

        # 4. Formato de solo fecha
        self.df['FECHA'] = self.df['FECHA'].dt._delegate_method

        # 5. Devolver dataframe
        return self.df