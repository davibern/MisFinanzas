"""
Test unitario para la clase CargarFicheroAhorro

Este archivo contiene tests unitarios para validar el funcionamiento de:
- Inicialización y parseo de archivos CSV de ahorros
- Limpieza y transformación de datos numéricos y de fechas
- Relleno de datos faltantes (ffill)
- Cálculo de columnas derivadas como TOTAL_APORTADO
"""

import pytest
import pandas as pd
from unittest.mock import patch
import datetime
from src.cargar_datos_ahorros import CargarFicheroAhorro


@pytest.fixture
def csv_sample_content() -> str:
    """
    Fixture: Crea contenido CSV de ejemplo para pruebas.

    Simula la estructura de un archivo CSV de ahorros con:
    - Fila de encabezados
    - Filas de datos con fechas, movimientos, importes y saldos en formato español
    - Filas con fechas y saldos faltantes para probar ffill

    Returns:
        str: Contenido CSV de ejemplo
    """
    return """FECHA,MOVIMIENTO,IMPORTE,SALDO
15/01/2025,Aportación inicial,"1.000,50","1.000,50"
,Intereses,,"1.010,00"
20/01/2025,Nueva aportación,"500,00","1.510,00"
"""


@pytest.fixture
def mock_csv_file(csv_sample_content: str, tmp_path):
    """
    Fixture: Crea un archivo CSV temporal para pruebas.

    Args:
        csv_sample_content: Contenido CSV de ejemplo
        tmp_path: Directorio temporal proporcionado por pytest

    Returns:
        Path: Ruta al archivo CSV temporal
    """
    csv_file = tmp_path / "test_ahorros.csv"
    csv_file.write_text(csv_sample_content, encoding='utf-8')
    return csv_file


@pytest.fixture
def cargar_ahorro_instance(mock_csv_file) -> CargarFicheroAhorro:
    """
    Fixture: Crea una instancia de CargarFicheroAhorro con archivo de prueba.

    Args:
        mock_csv_file: Archivo CSV temporal

    Returns:
        CargarFicheroAhorro: Instancia inicializada
    """
    return CargarFicheroAhorro(str(mock_csv_file))


# ============================================================================
# TESTS PARA __init__
# ============================================================================

def test_init_cargar_ahorro(mock_csv_file):
    """
    Test: Verifica que la inicialización de CargarFicheroAhorro sea correcta.

    Comprueba que los atributos se inicialicen correctamente.
    """
    # Act
    cargador = CargarFicheroAhorro(str(mock_csv_file))

    # Assert
    assert cargador.file == str(mock_csv_file)
    assert cargador.df is None


# ============================================================================
# TESTS PARA limpiar_datos
# ============================================================================

def test_limpiar_datos_carga_inicial(cargar_ahorro_instance: CargarFicheroAhorro):
    """
    Test: Verifica que read_csv cargue los datos correctamente.
    """
    # Act
    df = cargar_ahorro_instance.limpiar_datos()

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['FECHA', 'MOVIMIENTO', 'IMPORTE', 'SALDO', 'TOTAL_APORTADO']


def test_limpiar_datos_numeric_conversion(cargar_ahorro_instance: CargarFicheroAhorro):
    """
    Test: Verifica que IMPORTE y SALDO se limpien y conviertan a numérico.

    Comprueba que el símbolo €, puntos de miles y comas decimales se procesen bien.
    """
    # Act
    df = cargar_ahorro_instance.limpiar_datos()

    # Assert
    assert pd.api.types.is_float_dtype(df['IMPORTE'])
    assert pd.api.types.is_float_dtype(df['SALDO'])
    
    # Valores de IMPORTE (la fila de intereses tiene importe nulo, que se convierte a NaN)
    assert df['IMPORTE'].iloc[0] == 1000.50  # 1.000,50
    assert pd.isna(df['IMPORTE'].iloc[1])    # vacío
    assert df['IMPORTE'].iloc[2] == 500.00   # 500,00

    # Valores de SALDO
    assert df['SALDO'].iloc[0] == 1000.50    # 1.000,50
    assert df['SALDO'].iloc[1] == 1010.00    # 1.010,00
    assert df['SALDO'].iloc[2] == 1510.00    # 1.510,00


def test_limpiar_datos_date_processing(cargar_ahorro_instance: CargarFicheroAhorro):
    """
    Test: Verifica que FECHA se formatee correctamente y aplique ffill.

    Comprueba que las fechas se propaguen hacia abajo (ffill) y se conviertan a dt.date.
    """
    # Act
    df = cargar_ahorro_instance.limpiar_datos()

    # Assert
    # Verificar que el ffill ha funcionado en la fila 1 (índice 1) que no tenía fecha
    assert df['FECHA'].iloc[0] == datetime.date(2025, 1, 15)
    assert df['FECHA'].iloc[1] == datetime.date(2025, 1, 15)  # ffill
    assert df['FECHA'].iloc[2] == datetime.date(2025, 1, 20)

    # Verificar formato date
    for fecha in df['FECHA']:
        assert isinstance(fecha, datetime.date)


def test_limpiar_datos_remove_null_dates(tmp_path):
    """
    Test: Verifica que se eliminen filas que sigan sin fecha tras ffill.
    """
    # Arrange
    csv_invalid = """FECHA,MOVIMIENTO,IMPORTE,SALDO
INVALID,Aportación,"100,00","100,00"
"""
    csv_file = tmp_path / "test_invalid.csv"
    csv_file.write_text(csv_invalid, encoding='utf-8')
    
    cargador = CargarFicheroAhorro(str(csv_file))

    # Act
    df = cargador.limpiar_datos()

    # Assert
    assert len(df) == 0  # La fecha INVALID no pudo ser parseada, ffill no rellenó nada, debería eliminarse.


def test_limpiar_datos_text_format(cargar_ahorro_instance: CargarFicheroAhorro):
    """
    Test: Verifica que MOVIMIENTO sea convertido a formato string.
    """
    # Act
    df = cargar_ahorro_instance.limpiar_datos()

    # Assert
    assert pd.api.types.is_string_dtype(df['MOVIMIENTO'])
    assert df['MOVIMIENTO'].iloc[0] == "Aportación inicial"


def test_limpiar_datos_total_aportado(cargar_ahorro_instance: CargarFicheroAhorro):
    """
    Test: Verifica que TOTAL_APORTADO calcule correctamente la suma acumulada.
    """
    # Act
    df = cargar_ahorro_instance.limpiar_datos()

    # Assert
    assert 'TOTAL_APORTADO' in df.columns
    assert pd.api.types.is_float_dtype(df['TOTAL_APORTADO'])
    
    # 1.000,50 + 0 + 500,00
    assert df['TOTAL_APORTADO'].iloc[0] == 1000.50
    assert df['TOTAL_APORTADO'].iloc[1] == 1000.50
    assert df['TOTAL_APORTADO'].iloc[2] == 1500.50


def test_limpiar_datos_saldo_no_ffill(tmp_path):
    """
    Test: Verifica que SALDO deje como NaN los huecos vacíos.
    """
    # Arrange
    csv_saldo = """FECHA,MOVIMIENTO,IMPORTE,SALDO
01/01/2025,Mov1,"100,00","1.000,00"
02/01/2025,Mov2,"50,00",
"""
    csv_file = tmp_path / "test_saldo.csv"
    csv_file.write_text(csv_saldo, encoding='utf-8')
    
    cargador = CargarFicheroAhorro(str(csv_file))

    # Act
    df = cargador.limpiar_datos()

    # Assert
    # Ya no se hace ffill, debería ser NaN
    assert pd.isna(df['SALDO'].iloc[1])
