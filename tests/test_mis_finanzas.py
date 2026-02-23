"""
Test unitario de ejemplo para la clase MisFinanzas

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
from src.mis_finanzas import MisFinanzas


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
    datos = pd.DataFrame({
        'fecha': ['2025-01-01', '2025-01-01', '2025-01-02', '2025-02-01', '2025-02-01', '2025-02-02', '2025-01-15'],
        'año': [2025, 2025, 2025, 2025, 2025, 2025, 2025],
        'mes': [1, 1, 1, 2, 2, 2, 1],
        'tipo': ['Ingreso', 'Ingreso', 'Gasto', 'Ingreso', 'Gasto', 'Gasto', 'Gasto'],
        'categoria': ['Salario', 'Freelance', 'Alimentación', 'Salario', 'Transporte', 'Ocio', 'Planes de pensión y previsión'],
        'importe': [2000.0, 500.0, -150.0, 2000.0, -80.0, -120.0, -600.0]
    })
    return datos


@pytest.fixture
def mis_finanzas_mock(datos_prueba: pd.DataFrame) -> MisFinanzas:
    """
    Fixture: Crea una instancia de MisFinanzas con datos mockeados.

    Usamos @patch para evitar que se cargue el archivo real 'finanzas.parquet'
    y en su lugar usamos nuestros datos de prueba.

    Args:
        datos_prueba: Fixture con los datos de prueba

    Returns:
        MisFinanzas: Instancia de la clase con datos de prueba
    """
    with patch('pandas.read_parquet', return_value=datos_prueba):
        finanzas = MisFinanzas()
    return finanzas


# ============================================================================
# TESTS DE EJEMPLO
# ============================================================================

def test_obtener_ingresos_mes_año(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se calculen correctamente los ingresos de un mes.

    Patrón AAA (Arrange-Act-Assert):
    - Arrange: Preparar datos (ya hecho en el fixture)
    - Act: Ejecutar la función a probar
    - Assert: Verificar que el resultado es el esperado
    """
    # Act: Ejecutamos la función
    resultado = mis_finanzas_mock.obtener_ingresos_mes_año(2025, 1)

    # Assert: Verificamos que el resultado sea correcto
    # En enero 2025 tenemos: Salario (2000) + Freelance (500) = 2500
    assert resultado == 2500.0, f"Se esperaba 2500.0 pero se obtuvo {resultado}"


def test_obtener_gastos_mes_año(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se calculen correctamente los gastos de un mes.

    Los gastos en nuestros datos están en negativo, así que la suma
    debería dar un valor negativo.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_gastos_mes_año(2025, 1)

    # Assert
    # En enero 2025 tenemos: Alimentación (-150) + Planes de pensión (-600) = -750
    assert resultado == -750.0, f"Se esperaba -750.0 pero se obtuvo {resultado}"


def test_obtener_media_gastos_mes_año(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se calculen correctamente la media de gasto diario de un mes.

    El gasto diario es la suma de los gastos agrupados por fecha, y la media es el promedio de estos totales diarios.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_media_gastos_mes_año(2025, 1)

    # Assert
    # En enero 2025: Alimentación (-150) el día 02 y Planes de pensión (-600) el día 15
    # Media diaria = (150 + 600) / 2 = 375.0
    assert resultado == 375.0, f"Se esperaba 375.0 pero se obtuvo {resultado}"


def test_obtener_gastos_mes_sin_datos(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica el comportamiento cuando no hay datos para un mes.

    Este test comprueba un caso límite (edge case): ¿qué pasa si
    consultamos un mes que no tiene datos?
    """
    # Act
    resultado = mis_finanzas_mock.obtener_gastos_mes_año(2025, 12)

    # Assert
    # Debería devolver 0 porque no hay datos para diciembre
    assert resultado == 0.0, f"Se esperaba 0.0 pero se obtuvo {resultado}"


def test_obtener_intervalo_gastos(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se calculen correctamente los gastos en un intervalo.

    Este test prueba una función más compleja que trabaja con rangos de meses.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_intervalo_gastos(2025, 1, 2)

    # Assert
    # Gastos de enero a febrero: -150 + -600 (enero) + -80 + -120 (febrero) = -950
    assert resultado == -950.0, f"Se esperaba -950.0 pero se obtuvo {resultado}"


def test_obtener_gastos_agrupados_mes_año(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que los gastos se agrupen correctamente por categoría.

    Este test comprueba que la función devuelve un DataFrame con la
    estructura correcta y los valores esperados.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_gastos_agrupados_mes_año(2025, 2)

    # Assert
    # Verificamos que sea un DataFrame
    assert isinstance(resultado, pd.DataFrame), "El resultado debería ser un DataFrame"

    # Verificamos que tenga las columnas correctas
    assert 'categoria' in resultado.columns, "Debería tener columna 'categoria'"
    assert 'importe' in resultado.columns, "Debería tener columna 'importe'"

    # Verificamos el número de categorías
    assert len(resultado) == 2, f"Se esperaban 2 categorías pero se obtuvieron {len(resultado)}"

    # Verificamos que las categorías sean las correctas
    categorias_esperadas = {'Transporte', 'Ocio'}
    categorias_obtenidas = set(resultado['categoria'].values)
    assert categorias_obtenidas == categorias_esperadas, \
        f"Se esperaban {categorias_esperadas} pero se obtuvieron {categorias_obtenidas}"


def test_obtener_intervalo_ingresos_por_meses(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se obtengan correctamente los ingresos por mes.

    Este test comprueba que la función devuelve un DataFrame con
    los ingresos agrupados por mes.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_intervalo_ingresos_por_meses(2025)

    # Assert
    assert isinstance(resultado, pd.DataFrame), "El resultado debería ser un DataFrame"
    assert len(resultado) == 2, f"Se esperaban 2 meses pero se obtuvieron {len(resultado)}"

    # Verificamos los valores de cada mes
    mes_1 = resultado[resultado['mes'] == 1]['importe'].values[0]
    mes_2 = resultado[resultado['mes'] == 2]['importe'].values[0]

    assert mes_1 == 2500.0, f"Ingresos de enero deberían ser 2500.0 pero son {mes_1}"
    assert mes_2 == 2000.0, f"Ingresos de febrero deberían ser 2000.0 pero son {mes_2}"


def test_obtener_ahorro_jubilacion_por_meses(mis_finanzas_mock: MisFinanzas) -> None:
    """
    Test: Verifica que se obtengan correctamente los gastos por mes.

    Este test comprueba que la función devuelve un DataFrame con
    los gastos agrupados por mes.
    """
    # Act
    resultado = mis_finanzas_mock.obtener_ahorro_jubilacion_por_meses(2025)

    # Assert
    assert isinstance(resultado, pd.DataFrame), "El resultado debería ser un DataFrame"
    assert len(resultado) == 1, f"Se esperaba 1 mes pero se obtuvieron {len(resultado)}"

    # Verificamos el valor del ahorro en enero (el importe es negativo como los gastos)
    ahorro_enero = resultado[resultado['mes'] == 1]['importe'].values[0]
    assert ahorro_enero == 600.0, f"El ahorro de jubilación de enero debería ser 600.0 pero es {ahorro_enero}"
