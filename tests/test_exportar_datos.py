"""
Test unitario para la clase ExportarDatos

Este archivo contiene tests unitarios para validar el funcionamiento de:
- Validación de períodos (año/mes) ya procesados
- Exportación de datos a formato Parquet
- Manejo de particiones por año y mes
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.cargar_datos_bancarios import CargarFicheroBancario
from src.exportar_datos import ExportarDatos


@pytest.fixture
def datos_prueba_df() -> pd.DataFrame:
    """
    Fixture: Crea un DataFrame de prueba con datos de finanzas.

    Returns:
        pd.DataFrame: DataFrame con datos de ejemplo
    """
    return pd.DataFrame({
        'fecha': pd.to_datetime(['2025-01-15', '2025-01-20', '2025-02-10']),
        'concepto': ['Salario', 'Supermercado', 'Gasolina'],
        'categoria': ['Nómina', 'Alimentación', 'Transporte'],
        'importe': [2000.0, -150.0, -50.0],
        'tipo_movimiento': ['Ingreso', 'Gasto', 'Gasto'],
        'cuenta_tarjeta': ['Cuenta Principal', 'Tarjeta', 'Tarjeta'],
        'tipo': ['Ingreso', 'Gasto', 'Gasto'],
        'mes': [1, 1, 2],
        'año': [2025, 2025, 2025],
        'mes_nombre': ['January', 'January', 'February'],
        'dia_semana': ['Wednesday', 'Monday', 'Monday']
    })


@pytest.fixture
def mock_cargar_fichero(datos_prueba_df: pd.DataFrame) -> CargarFicheroBancario:
    """
    Fixture: Crea un mock de CargarFichero con datos de prueba.

    Args:
        datos_prueba_df: DataFrame de prueba

    Returns:
        Mock: Mock de CargarFichero con DataFrame asignado
    """
    mock = Mock(spec=CargarFicheroBancario)
    mock.df = datos_prueba_df
    return mock


@pytest.fixture
def exportar_datos_instance(mock_cargar_fichero: CargarFicheroBancario) -> ExportarDatos:
    """
    Fixture: Crea una instancia de ExportarDatos con datos de prueba.

    Args:
        mock_cargar_fichero: Mock de CargarFichero

    Returns:
        ExportarDatos: Instancia inicializada
    """
    return ExportarDatos(mock_cargar_fichero, tipo='bancario')


# ============================================================================
# TESTS PARA __init__
# ============================================================================

def test_init_exportar_datos(mock_cargar_fichero: CargarFicheroBancario):
    """
    Test: Verifica que la inicialización de ExportarDatos sea correcta.

    Comprueba que el atributo datos se asigne correctamente.
    """
    # Act
    exportador = ExportarDatos(mock_cargar_fichero, tipo='bancario')

    # Assert
    assert exportador.datos == mock_cargar_fichero
    assert exportador.datos.df is not None
    assert exportador.tipo == 'bancario'


# ============================================================================
# TESTS PARA validar_año_mes
# ============================================================================

def test_validar_año_mes_file_not_found(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica el comportamiento cuando el archivo parquet no existe.

    Cuando no existe el archivo, debe devolver False (no hay datos previos).
    """
    # Arrange
    with patch('pandas.read_parquet', side_effect=FileNotFoundError()):
        # Act
        resultado = exportar_datos_instance.validar_año_mes()

        # Assert
        assert resultado is False


def test_validar_año_mes_new_periods_exist(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que devuelva True cuando todos los períodos ya existen.

    Si todos los pares (año, mes) de los nuevos datos ya están en el archivo,
    debe devolver True.
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [2025, 2025, 2025],
        'mes': [1, 1, 2],
        'importe': [1000.0, -200.0, -100.0]
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        # Act
        resultado = exportar_datos_instance.validar_año_mes()

        # Assert
        assert resultado is True


def test_validar_año_mes_new_periods_not_exist(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que devuelva False cuando hay períodos nuevos.

    Si hay al menos un par (año, mes) que no existe en el archivo,
    debe devolver False.
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [2024, 2024],
        'mes': [11, 12],
        'importe': [1000.0, -200.0]
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        # Act
        resultado = exportar_datos_instance.validar_año_mes()

        # Assert
        assert resultado is False


def test_validar_año_mes_mixed_periods(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica el comportamiento con períodos mixtos (algunos nuevos, algunos existentes).

    Si hay al menos un período nuevo, debe devolver False.
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [2025, 2025],
        'mes': [1, 1],
        'importe': [1000.0, -200.0]
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        # Act
        resultado = exportar_datos_instance.validar_año_mes()

        # Assert
        # Tenemos mes 1 (existe) y mes 2 (no existe), por lo que debe ser False
        assert resultado is False


def test_validar_año_mes_empty_existing_file(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica el comportamiento con un archivo existente vacío.

    Si el archivo existe pero está vacío, debe devolver False.
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [],
        'mes': [],
        'importe': []
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        # Act
        resultado = exportar_datos_instance.validar_año_mes()

        # Assert
        assert resultado is False


# ============================================================================
# TESTS PARA exportar
# ============================================================================

def test_exportar_when_validation_false(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que se exporte cuando la validación devuelve False.

    Cuando hay períodos nuevos, debe exportar y devolver 1.
    """
    # Arrange
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=False):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            resultado = exportar_datos_instance.exportar_parquet()

            # Assert
            assert resultado == 1
            mock_to_parquet.assert_called_once()


def test_exportar_when_validation_true(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que NO se exporte cuando la validación devuelve True.

    Cuando todos los períodos ya existen, debe devolver 0 sin exportar.
    """
    # Arrange
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=True):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            resultado = exportar_datos_instance.exportar_parquet()

            # Assert
            assert resultado == 0
            mock_to_parquet.assert_not_called()


def test_exportar_parquet_parameters(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que se usen los parámetros correctos al exportar.

    Comprueba que se llame a to_parquet con:
    - Ruta correcta
    - Engine pyarrow
    - Compresión snappy
    - Particiones por año y mes
    - Sin índice
    """
    # Arrange
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=False):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            exportar_datos_instance.exportar_parquet()

            # Assert
            mock_to_parquet.assert_called_once_with(
                "data/finanzas.parquet",
                engine="pyarrow",
                compression="snappy",
                partition_cols=["año", "mes"],
                index=False
            )


def test_exportar_creates_partitions(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que se especifiquen las columnas de partición correctas.

    Las particiones deben ser por año y mes.
    """
    # Arrange
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=False):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            exportar_datos_instance.exportar_parquet()

            # Assert
            call_kwargs = mock_to_parquet.call_args[1]
            assert call_kwargs['partition_cols'] == ["año", "mes"]


def test_exportar_return_values(exportar_datos_instance: ExportarDatos):
    """
    Test: Verifica que los valores de retorno sean correctos.

    Debe devolver:
    - 1 cuando se exporta
    - 0 cuando no se exporta
    """
    # Arrange & Act & Assert - Caso 1: Se exporta
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=False):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet'):
            resultado = exportar_datos_instance.exportar_parquet()
            assert resultado == 1

    # Arrange & Act & Assert - Caso 2: No se exporta
    with patch.object(exportar_datos_instance, 'validar_año_mes', return_value=True):
        resultado = exportar_datos_instance.exportar_parquet()
        assert resultado == 0


# ============================================================================
# TESTS DE INTEGRACIÓN
# ============================================================================

def test_integration_validar_and_exportar(exportar_datos_instance: ExportarDatos):
    """
    Test de integración: Verifica el flujo completo de validación y exportación.

    Simula un escenario real donde:
    1. Se valida si los datos ya existen
    2. Se exporta solo si hay datos nuevos
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [2024],
        'mes': [12],
        'importe': [1000.0]
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            resultado = exportar_datos_instance.exportar_parquet()

            # Assert
            # Como los datos de prueba son de 2025/01 y 2025/02, y solo existe 2024/12,
            # debe exportar
            assert resultado == 1
            mock_to_parquet.assert_called_once()


def test_integration_duplicate_prevention(exportar_datos_instance: ExportarDatos):
    """
    Test de integración: Verifica que se prevengan duplicados.

    Si intentamos exportar datos que ya existen, no debe hacer nada.
    """
    # Arrange
    df_existente = pd.DataFrame({
        'año': [2025, 2025, 2025],
        'mes': [1, 1, 2],
        'importe': [1000.0, -200.0, -100.0]
    })

    with patch('pandas.read_parquet', return_value=df_existente):
        with patch.object(exportar_datos_instance.datos.df, 'to_parquet') as mock_to_parquet:
            # Act
            resultado = exportar_datos_instance.exportar_parquet()

            # Assert
            # Como todos los períodos ya existen, no debe exportar
            assert resultado == 0
            mock_to_parquet.assert_not_called()
