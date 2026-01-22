import pandas as pd
import re
from lxml import etree


class CargarFichero:
    def __init__(self, file):
        self.file: str = file
        self.data: list = []
        self.headers: list = []
        self.header_found: bool = False
        self.df: pd.DataFrame = None

    def parsear_xml(self):
        """
        Parsea el archivo XML de finanzas y extrae los datos en un DataFrame

        Returns:
            DataFrame con los datos procesados
        """

        # Parsear el fichero XML
        tree = etree.parse(self.file)
        root = tree.getroot()

        # Definir namespaces
        namespaces = {
            'ss': 'urn:schemas-microsoft-com:office:spreadsheet',
            'o': 'urn:schemas-microsoft-com:office:office',
            'x': 'urn:schemas-microsoft-com:office:excel',
            'html': 'http://www.w3.org/TR/REC-html40'
        }

        # Encontrar las filas de la tabla
        rows = root.xpath('//ss:Worksheet[@ss:Name="Ingresos y Gastos"]//ss:Row', namespaces=namespaces)

        # Extraer datos
        for row in rows:
            cells = row.xpath('.//ss:Cell', namespaces=namespaces)
            row_data = []

            for cell in cells:
                # Obtener el valor de la celda
                data_elem = cell.xpath('.//ss:Data', namespaces=namespaces)
                if data_elem:
                    value = data_elem[0].text
                    row_data.append(value if value is not None else '')
                else:
                    row_data.append('')

            # Buscar la fila de encabezados
            if not self.header_found and row_data and 'Fecha' in row_data:
                self.headers = [h for h in row_data if h]
                self.header_found = True
                continue

            # Extraer filas de datos (deben tener una fecha válida)
            if self.header_found and row_data:
                first_value = row_data[0] if row_data else ''
                if first_value and re.match(r'\d{2}/\d{2}/\d{4}', first_value):
                    # Sólo toma las columnas que corresponde a los encabezados
                    self.data.append(row_data[:len(self.headers)])

        # Crear DataFrame
        self.df = pd.DataFrame(self.data, columns=self.headers)

        return self.df

    def limpiar_datos(self):
        """
        Limpia y procesa los datos del DataFrame

        Returns:
            DataFrame limpio y procesado
        """

        # Renombrar columnas
        column_mapping = {
            'Fecha': 'fecha',
            'Concepto': 'concepto',
            'Categoría': 'categoría',
            'Importe (€)': 'importe',
            'Tipo Movimiento': 'tipo_movimiento',
            'Cuenta/Tarjeta': 'cuenta_tarjeta'
        }

        self.df.rename(columns=column_mapping, inplace=True)

        # Convertir fecha a datetime
        self.df['fecha'] = pd.to_datetime(self.df['fecha'], format='%d/%m/%Y', errors='coerce')

        # Convertir importe a numérico
        self.df['importe'] = self.df['importe'].astype(str).str.replace(',', '.').str.replace(' ', '').astype(float)
        self.df['importe'] = pd.to_numeric(self.df['importe'], errors='coerce')

        # Crear columna de tipo simplificada
        self.df['tipo'] = self.df['tipo_movimiento'].str.extract(r'(Ingreso|Gasto)', expand=False)

        # Limpiar espacios no separables en cuenta_tarjeta
        self.df['cuenta_tarjeta'] = self.df['cuenta_tarjeta'].str.replace('\xa0', ' ')

        # Eliminar filas con fecha nula
        self.df = self.df.dropna(subset=['fecha'])

        # Ordenar por fecha descendente
        self.df = self.df.sort_values('fecha', ascending=False).reset_index(drop=True)

        # Añadir columnas útiles
        self.df['mes'] = self.df['fecha'].dt.month
        self.df['año'] = self.df['fecha'].dt.year
        self.df['mes_nombre'] = self.df['fecha'].dt.strftime('%B')
        self.df['dia_semana'] = self.df['fecha'].dt.day_name()

        return self.df
