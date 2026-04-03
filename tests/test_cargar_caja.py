"""
Test unitario para la clase CargarFicheroCaja

Este archivo contiene tests unitarios para validar el funcionamiento de:
- Inicialización y parseo de archivos CSV del flujo de caja
- Limpieza y transformación de datos numéricos y de fechas
"""

import pytest
import pandas as pd
import datetime
from src.cargar_datos_caja import CargarFicheroCaja

@pytest.fixture
def csv_sample_content() -> str:
    """
    Fixture: Crea contenido CSV de ejemplo para pruebas.
    """
    return """FECHA,CAJA
05/07/2024,"€10.891,38"
,"€17.829,63"
05/09/2024,"€19.038,27"
"""

@pytest.fixture
def mock_csv_file(csv_sample_content: str, tmp_path):
    """
    Fixture: Crea un archivo CSV temporal para pruebas.
    """
    csv_file = tmp_path / "test_caja.csv"
    csv_file.write_text(csv_sample_content, encoding='utf-8')
    return csv_file

@pytest.fixture
def cargar_caja_instance(mock_csv_file) -> CargarFicheroCaja:
    """
    Fixture: Crea una instancia de CargarFicheroCaja.
    """
    return CargarFicheroCaja(str(mock_csv_file))

# ============================================================================
# TESTS PARA __init__
# ============================================================================

def test_init_cargar_caja(mock_csv_file):
    cargador = CargarFicheroCaja(str(mock_csv_file))
    assert cargador.file == str(mock_csv_file)
    assert cargador.df is None

# ============================================================================
# TESTS PARA limpiar_datos
# ============================================================================

def test_limpiar_datos_carga_inicial(cargar_caja_instance: CargarFicheroCaja):
    df = cargar_caja_instance.limpiar_datos()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['FECHA', 'CAJA']

def test_limpiar_datos_numeric_conversion(cargar_caja_instance: CargarFicheroCaja):
    df = cargar_caja_instance.limpiar_datos()
    
    assert pd.api.types.is_float_dtype(df['CAJA'])
    
    assert df['CAJA'].iloc[0] == 10891.38
    assert df['CAJA'].iloc[1] == 17829.63
    assert df['CAJA'].iloc[2] == 19038.27

def test_limpiar_datos_date_processing(cargar_caja_instance: CargarFicheroCaja):
    df = cargar_caja_instance.limpiar_datos()
    
    # Comprobar ffill en índice 1 (que no tiene fecha original)
    assert df['FECHA'].iloc[0] == datetime.date(2024, 7, 5)
    assert df['FECHA'].iloc[1] == datetime.date(2024, 7, 5)  # ffill
    assert df['FECHA'].iloc[2] == datetime.date(2024, 9, 5)

    for fecha in df['FECHA']:
        assert isinstance(fecha, datetime.date)
