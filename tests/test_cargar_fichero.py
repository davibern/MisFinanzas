"""
Test unitario para la clase CargarFichero

Este archivo contiene tests unitarios para validar el funcionamiento de:
- Parseo de archivos XML con formato específico de finanzas
- Limpieza y transformación de datos
- Manejo de errores y casos límite
"""

import pytest
import pandas as pd
from lxml import etree
from unittest.mock import patch
from src.cargar_datos_bancarios import CargarFicheroBancario as CargarFichero


@pytest.fixture
def xml_sample_content() -> str:
    """
    Fixture: Crea contenido XML de ejemplo para pruebas.

    Simula la estructura de un archivo XML de finanzas con:
    - Namespaces correctos
    - Hoja de trabajo "Ingresos y Gastos"
    - Fila de encabezados
    - Filas de datos con fechas válidas

    Returns:
        str: Contenido XML de ejemplo
    """
    return """<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:x="urn:schemas-microsoft-com:office:excel"
 xmlns:html="http://www.w3.org/TR/REC-html40">
 <Worksheet ss:Name="Ingresos y Gastos">
  <Table>
   <Row>
    <Cell><Data ss:Type="String">Fecha</Data></Cell>
    <Cell><Data ss:Type="String">Concepto</Data></Cell>
    <Cell><Data ss:Type="String">Categoría</Data></Cell>
    <Cell><Data ss:Type="String">Importe (€)</Data></Cell>
    <Cell><Data ss:Type="String">Tipo Movimiento</Data></Cell>
    <Cell><Data ss:Type="String">Cuenta/Tarjeta</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="String">15/01/2025</Data></Cell>
    <Cell><Data ss:Type="String">Salario</Data></Cell>
    <Cell><Data ss:Type="String">Nómina</Data></Cell>
    <Cell><Data ss:Type="String">2000,50</Data></Cell>
    <Cell><Data ss:Type="String">Ingreso</Data></Cell>
    <Cell><Data ss:Type="String">Cuenta Principal</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="String">20/01/2025</Data></Cell>
    <Cell><Data ss:Type="String">Supermercado</Data></Cell>
    <Cell><Data ss:Type="String">Alimentación</Data></Cell>
    <Cell><Data ss:Type="String">150,75</Data></Cell>
    <Cell><Data ss:Type="String">Gasto</Data></Cell>
    <Cell><Data ss:Type="String">Tarjeta Débito</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
</Workbook>"""


@pytest.fixture
def mock_xml_file(xml_sample_content: str, tmp_path):
    """
    Fixture: Crea un archivo XML temporal para pruebas.

    Args:
        xml_sample_content: Contenido XML de ejemplo
        tmp_path: Directorio temporal proporcionado por pytest

    Returns:
        Path: Ruta al archivo XML temporal
    """
    xml_file = tmp_path / "test_finanzas.xml"
    xml_file.write_text(xml_sample_content, encoding='utf-8')
    return xml_file


@pytest.fixture
def cargar_fichero_instance(mock_xml_file) -> CargarFichero:
    """
    Fixture: Crea una instancia de CargarFichero con archivo de prueba.

    Args:
        mock_xml_file: Archivo XML temporal

    Returns:
        CargarFichero: Instancia inicializada
    """
    return CargarFichero(str(mock_xml_file))


# ============================================================================
# TESTS PARA __init__
# ============================================================================

def test_init_cargar_fichero(mock_xml_file):
    """
    Test: Verifica que la inicialización de CargarFichero sea correcta.

    Comprueba que todos los atributos se inicialicen con valores apropiados.
    """
    # Act
    cargador = CargarFichero(str(mock_xml_file))

    # Assert
    assert cargador.file == str(mock_xml_file)
    assert cargador.data == []
    assert cargador.headers == []
    assert cargador.header_found is False
    assert cargador.df is None


# ============================================================================
# TESTS PARA parsear_xml
# ============================================================================

def test_parsear_xml_success(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que el parseo XML funcione correctamente.

    Comprueba que:
    - Se cree un DataFrame
    - Tenga las columnas correctas
    - Tenga el número correcto de filas
    """
    # Act
    df = cargar_fichero_instance.parsear_xml()

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2  # 2 filas de datos
    assert list(df.columns) == ['Fecha', 'Concepto', 'Categoría', 'Importe (€)', 'Tipo Movimiento', 'Cuenta/Tarjeta']


def test_parsear_xml_header_detection(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que se detecten correctamente los encabezados.

    Comprueba que la fila de encabezados se identifique y no se incluya en los datos.
    """
    # Act
    cargar_fichero_instance.parsear_xml()

    # Assert
    assert cargar_fichero_instance.header_found is True
    assert 'Fecha' in cargar_fichero_instance.headers
    assert len(cargar_fichero_instance.headers) == 6


def test_parsear_xml_data_extraction(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que se extraigan correctamente los datos.

    Comprueba que los valores de las celdas se lean correctamente.
    """
    # Act
    df = cargar_fichero_instance.parsear_xml()

    # Assert
    assert df.iloc[0]['Fecha'] == '15/01/2025'
    assert df.iloc[0]['Concepto'] == 'Salario'
    assert df.iloc[1]['Fecha'] == '20/01/2025'
    assert df.iloc[1]['Concepto'] == 'Supermercado'


def test_parsear_xml_date_validation(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que solo se incluyan filas con fechas válidas.

    Las filas sin fecha en formato DD/MM/YYYY no deben incluirse.
    """
    # Act
    df = cargar_fichero_instance.parsear_xml()

    # Assert
    # Todas las filas deben tener fechas válidas
    for fecha in df['Fecha']:
        assert pd.notna(fecha)
        assert len(fecha.split('/')) == 3


def test_parsear_xml_empty_worksheet():
    """
    Test: Verifica el comportamiento con una hoja de trabajo vacía.

    Comprueba que se maneje correctamente un XML sin datos.
    """
    # Arrange
    empty_xml = """<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Worksheet ss:Name="Ingresos y Gastos">
  <Table>
  </Table>
 </Worksheet>
</Workbook>"""

    with patch('lxml.etree.parse') as mock_parse:
        mock_tree = etree.fromstring(empty_xml.encode('utf-8'))
        mock_parse.return_value = etree.ElementTree(mock_tree)

        # Act
        cargador = CargarFichero("dummy.xml")
        df = cargador.parsear_xml()

        # Assert
        assert len(df) == 0


# ============================================================================
# TESTS PARA limpiar_datos
# ============================================================================

def test_limpiar_datos_column_renaming(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que las columnas se renombren correctamente.

    Comprueba que los nombres de columnas en español se conviertan a minúsculas.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    expected_columns = ['fecha', 'concepto', 'categoria', 'importe', 'tipo_movimiento', 'cuenta_tarjeta']
    assert all(col in df.columns for col in expected_columns)


def test_limpiar_datos_date_conversion(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que las fechas se conviertan a datetime.

    Comprueba que la columna 'fecha' sea de tipo datetime64.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    assert pd.api.types.is_datetime64_any_dtype(df['fecha'])
    # Los datos se ordenan por fecha descendente, así que la primera fila es la más reciente
    assert df['fecha'].iloc[0] == pd.Timestamp('2025-01-20')


def test_limpiar_datos_numeric_conversion(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que los importes se conviertan a numérico.

    Comprueba que:
    - Las comas se reemplacen por puntos
    - Los valores sean de tipo float
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    assert pd.api.types.is_float_dtype(df['importe'])
    # Los datos se ordenan por fecha descendente (20/01 primero, luego 15/01)
    assert df['importe'].iloc[0] == 150.75  # Supermercado (20/01)
    assert df['importe'].iloc[1] == 2000.50  # Salario (15/01)


def test_limpiar_datos_tipo_extraction(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que se extraiga correctamente el tipo (Ingreso/Gasto).

    Comprueba que la columna 'tipo' contenga solo 'Ingreso' o 'Gasto'.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    assert 'tipo' in df.columns
    # Los datos se ordenan por fecha descendente (20/01 primero, luego 15/01)
    assert df['tipo'].iloc[0] == 'Gasto'  # Supermercado (20/01)
    assert df['tipo'].iloc[1] == 'Ingreso'  # Salario (15/01)


def test_limpiar_datos_sorting(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que los datos se ordenen por fecha descendente.

    Comprueba que la fecha más reciente esté primero.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    # La fecha 20/01/2025 debe estar antes que 15/01/2025
    assert df['fecha'].iloc[0] > df['fecha'].iloc[1]


def test_limpiar_datos_helper_columns(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que se añadan las columnas auxiliares.

    Comprueba que se creen las columnas: mes, año, mes_nombre, dia_semana.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    assert 'mes' in df.columns
    assert 'año' in df.columns
    assert 'mes_nombre' in df.columns
    assert 'dia_semana' in df.columns

    # Verificar tipos
    assert df['mes'].dtype == int
    assert df['año'].dtype == int

    # Verificar valores
    assert df['mes'].iloc[0] == 1  # Enero
    assert df['año'].iloc[0] == 2025


def test_limpiar_datos_remove_null_dates():
    """
    Test: Verifica que se eliminen filas con fechas nulas.

    Comprueba que las filas con fechas inválidas no aparezcan en el resultado.
    """
    # Arrange
    xml_with_invalid = """<?xml version="1.0"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"
 xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
 <Worksheet ss:Name="Ingresos y Gastos">
  <Table>
   <Row>
    <Cell><Data ss:Type="String">Fecha</Data></Cell>
    <Cell><Data ss:Type="String">Concepto</Data></Cell>
    <Cell><Data ss:Type="String">Categoría</Data></Cell>
    <Cell><Data ss:Type="String">Importe (€)</Data></Cell>
    <Cell><Data ss:Type="String">Tipo Movimiento</Data></Cell>
    <Cell><Data ss:Type="String">Cuenta/Tarjeta</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="String">15/01/2025</Data></Cell>
    <Cell><Data ss:Type="String">Salario</Data></Cell>
    <Cell><Data ss:Type="String">Nómina</Data></Cell>
    <Cell><Data ss:Type="String">2000</Data></Cell>
    <Cell><Data ss:Type="String">Ingreso</Data></Cell>
    <Cell><Data ss:Type="String">Cuenta</Data></Cell>
   </Row>
   <Row>
    <Cell><Data ss:Type="String">INVALID</Data></Cell>
    <Cell><Data ss:Type="String">Test</Data></Cell>
    <Cell><Data ss:Type="String">Test</Data></Cell>
    <Cell><Data ss:Type="String">100</Data></Cell>
    <Cell><Data ss:Type="String">Gasto</Data></Cell>
    <Cell><Data ss:Type="String">Cuenta</Data></Cell>
   </Row>
  </Table>
 </Worksheet>
</Workbook>"""

    with patch('lxml.etree.parse') as mock_parse:
        mock_tree = etree.fromstring(xml_with_invalid.encode('utf-8'))
        mock_parse.return_value = etree.ElementTree(mock_tree)

        # Act
        cargador = CargarFichero("dummy.xml")
        cargador.parsear_xml()
        df = cargador.limpiar_datos()

        # Assert
        # Solo debe haber 1 fila (la válida)
        assert len(df) == 1
        assert df['concepto'].iloc[0] == 'Salario'


def test_limpiar_datos_cuenta_tarjeta_cleaning(cargar_fichero_instance: CargarFichero):
    """
    Test: Verifica que se limpien espacios no separables en cuenta_tarjeta.

    Comprueba que los caracteres \\xa0 se reemplacen por espacios normales.
    """
    # Arrange
    cargar_fichero_instance.parsear_xml()

    # Act
    df = cargar_fichero_instance.limpiar_datos()

    # Assert
    # Verificar que no haya caracteres \\xa0
    for valor in df['cuenta_tarjeta']:
        assert '\\xa0' not in valor
