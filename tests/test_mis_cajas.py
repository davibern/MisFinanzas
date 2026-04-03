"""
Test unitario para la clase MisCajas

Este archivo contiene los tests unitarios para verificar el correcto
funcionamiento de los métodos de la clase MisCajas en src.mis_cajas.
"""

import pytest
import pandas as pd
from unittest.mock import patch
from src.mis_cajas import MisCajas


@pytest.fixture
def datos_prueba() -> pd.DataFrame:
    """
    Fixture: Crea datos de prueba para usar en los tests.

    Returns:
        pd.DataFrame: DataFrame con datos de prueba simulados
    """
    # Creamos un DataFrame con 12 meses de datos para 'CAJA'
    datos = pd.DataFrame({
        'FECHA': pd.date_range(start='2024-01-01', periods=12, freq='ME'),
        'CAJA': [100.0, 200.0, 150.0, 300.0, 250.0, 400.0, 350.0, 500.0, 450.0, 600.0, 550.0, 700.0]
    })
    return datos


@pytest.fixture
def mis_cajas_mock(datos_prueba: pd.DataFrame) -> MisCajas:
    """
    Fixture: Crea una instancia de MisCajas con datos mockeados.

    Usamos @patch para evitar que se llame a cargar_datos_caja.
    """
    with patch('src.mis_cajas.cargar_datos_caja', return_value=datos_prueba):
        cajas = MisCajas()
    return cajas


def test_obtener_historico(mis_cajas_mock: MisCajas, datos_prueba: pd.DataFrame) -> None:
    """
    Test: Verifica que obtener_historico devuelve los datos esperados.
    """
    resultado = mis_cajas_mock.obtener_historico()

    assert isinstance(resultado, pd.DataFrame)
    pd.testing.assert_frame_equal(resultado, datos_prueba)


def test_obtener_media_caja_3_meses(mis_cajas_mock: MisCajas, datos_prueba: pd.DataFrame) -> None:
    """
    Test: Verifica el cálculo de la media de los últimos 3 meses.
    """
    resultado = mis_cajas_mock.obtener_media_caja_3_meses()
    esperado = datos_prueba['CAJA'].tail(3).mean()
    
    assert resultado == esperado
    # 600.0 + 550.0 + 700.0 = 1850.0 -> / 3 = 616.666...
    assert round(resultado, 2) == 616.67


def test_obtener_media_caja_6_meses(mis_cajas_mock: MisCajas, datos_prueba: pd.DataFrame) -> None:
    """
    Test: Verifica el cálculo de la media de los últimos 6 meses.
    """
    resultado = mis_cajas_mock.obtener_media_caja_6_meses()
    esperado = datos_prueba['CAJA'].tail(6).mean()
    
    assert resultado == esperado
    # 350 + 500 + 450 + 600 + 550 + 700 = 3150 -> / 6 = 525.0
    assert resultado == 525.0


def test_obtener_media_caja_12_meses(mis_cajas_mock: MisCajas, datos_prueba: pd.DataFrame) -> None:
    """
    Test: Verifica el cálculo de la media de los últimos 12 meses.
    """
    resultado = mis_cajas_mock.obtener_media_caja_12_meses()
    esperado = datos_prueba['CAJA'].tail(12).mean()
    
    assert resultado == esperado
    # Suma de los 12 valores = 4550 -> / 12 = 379.1666...
    assert round(resultado, 2) == 379.17
