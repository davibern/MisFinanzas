"""
Test unitario de ejemplo para la clase MisAhorros

Este archivo demuestra cómo crear tests unitarios en Python usando pytest.
Incluye ejemplos de:
- Configuración de fixtures (datos de prueba)
- Tests básicos de funciones
- Uso de mocks para evitar dependencias de archivos reales
- Assertions (comprobaciones) de resultados
"""

import pytest
import pandas as pd
from unittest.mock import patch
from src.mis_ahorros import MisAhorros


@pytest.fixture
def datos_prueba() -> pd.DataFrame:
    """
    Fixture: Crea datos de prueba para usar en los tests.

    Un fixture es una función que se ejecuta antes de cada test
    y proporciona datos o configuración necesaria.

    Returns:
        pd.DataFrame: DataFrame con datos de prueba simulados
    """
    # Creamos un DataFrame con datos de ejemplo
    # Nota: incluimos dos conceptos de pensión distintos (AXA y FIATC) para
    # reflejar la estructura real de los datos y testear el groupby por concepto
    datos = pd.DataFrame({
        'FECHA': ['2025-01-01', '2025-02-01', '2025-03-01'],
        'MOVIMIENTO':   ['APORTACION INICIAL', 'APORTACION PERIÓDICA', 'APORTACION PERIÓDICA'],
        'IMPORTE':   [50.0, 50.0, 50.0],
        'TOTAL_APORTADO':  [50.0, 100.0, 150.0],
        'SALDO': [50.0, 110.0, 160.0]
    })
    return datos


@pytest.fixture
def mis_ahorros_mock(datos_prueba: pd.DataFrame) -> MisAhorros:
    """
    Fixture: Crea una instancia de MisAhorros con datos mockeados.

    Usamos @patch para evitar que se cargue el archivo real 'finanzas.parquet'
    y en su lugar usamos nuestros datos de prueba.

    Args:
        datos_prueba: Fixture con los datos de prueba

    Returns:
        MisAhorros: Instancia de la clase con datos de prueba
    """
    with patch('src.mis_ahorros.pd.read_parquet', return_value=datos_prueba):
        ahorros = MisAhorros('FIATC')
    return ahorros


def test_obtener_historico(mis_ahorros_mock: MisAhorros, datos_prueba: pd.DataFrame) -> None:
    """
    Test: Verifica que obtener_historico devuelve los datos esperados.
    """
    # Llama al método bajo prueba
    resultado = mis_ahorros_mock.obtener_historico()

    # Comprueba que el resultado es un DataFrame
    assert isinstance(resultado, pd.DataFrame)

    # Comprueba que los datos devueltos coinciden con los datos de prueba
    pd.testing.assert_frame_equal(resultado, datos_prueba)

