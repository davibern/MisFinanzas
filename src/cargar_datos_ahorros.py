import pandas as pd


class CargarDatosAhorros:
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
        for col in ['IMPORTE', 'SALDO']:
            self.df[col] = (
                self.df[col].astype(str)
                .str.replace('€', '', regex=False)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.strip()
            )
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # 3. Procesar Fechas (Rellenar los huecos que mencionaste)
        self.df['FECHA'] = pd.to_datetime(self.df['FECHA'], dayfirst=True, errors='coerce')
        self.df['FECHA'] = self.df['FECHA'].ffill()

        # Eliminar filas que sigan sin fecha (como cabeceras corruptas)
        self.df = self.df.dropna(subset=['FECHA'])

        # Formato de solo fecha
        self.df['FECHA'] = self.df['FECHA'].dt.date

        # 4. Rellenar huecos del Saldo
        self.df['SALDO'] = self.df['SALDO'].ffill()

        # 5. Formato de texto para Movimiento
        self.df['MOVIMIENTO'] = self.df['MOVIMIENTO'].astype('string')

        # Opcional: retornar el df por si quieres encadenar métodos
        return self.df
