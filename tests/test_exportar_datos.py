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
from src.cargar_datos_ibkr import CargarCarteraIBKR
from src.exportar_datos import ExportarDatos
from src.config import RUTA_FINANZAS_PARQUET, RUTA_BOLSA_CARTERA


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
                RUTA_FINANZAS_PARQUET,
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


# ============================================================================
# TESTS PARA validar_fecha Y tipo='bolsa'
# ============================================================================

@pytest.fixture
def mock_cargar_ibkr_df() -> pd.DataFrame:
    """Fixture con DataFrame procesado de cartera IBKR."""
    return pd.DataFrame({
        "fecha": pd.to_datetime(["2026-11-10", "2026-11-10"]),
        "symbol": ["IBE", "AAPL"],
        "description": ["IBERDROLA SA", "APPLE INC"],
        "currency": ["EUR", "USD"],
        "quantity": [10.0, 5.0],
        "mark_price": [20.0, 150.0],
        "cost_basis_price": [18.0, 140.0],
        "cost_basis_money": [180.0, 700.0],
        "position_value": [200.0, 750.0],
        "fifo_pnl_unrealized": [20.0, 50.0],
        "fx_rate_to_base": [1.0, 0.9],
        "cost_basis_eur": [180.0, 630.0],
        "position_value_eur": [200.0, 675.0],
        "unrealized_pnl_eur": [20.0, 45.0],
        "pnl_percent": [11.11, 7.14],
        "percent_of_nav": [50.0, 50.0],
        "año": [2026, 2026],
    })


@pytest.fixture
def mock_cargador_ibkr(mock_cargar_ibkr_df: pd.DataFrame) -> CargarCarteraIBKR:
    """Fixture que crea un mock de CargarCarteraIBKR."""
    mock = Mock(spec=CargarCarteraIBKR)
    mock.df = mock_cargar_ibkr_df
    return mock


def test_validar_fecha_file_not_found(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que si no existe bolsa_cartera.parquet, validar_fecha devuelve False."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    with patch("pandas.read_parquet", side_effect=FileNotFoundError()):
        assert exportador.validar_fecha() is False


def test_validar_fecha_date_exists(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que devuelva True si la fecha ya existe en el parquet."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    df_existente = pd.DataFrame({"fecha": pd.to_datetime(["2026-11-10", "2026-11-09"])})
    with patch("pandas.read_parquet", return_value=df_existente):
        assert exportador.validar_fecha() is True


def test_validar_fecha_date_not_exists(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que devuelva False si la fecha es nueva."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    df_existente = pd.DataFrame({"fecha": pd.to_datetime(["2026-11-09"])})
    with patch("pandas.read_parquet", return_value=df_existente):
        assert exportador.validar_fecha() is False


def test_exportar_bolsa_when_validation_true(mock_cargador_ibkr: CargarCarteraIBKR):
    """Si la fecha ya existe, exportar_parquet devuelve 0 y no exporta."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    with patch.object(exportador, "validar_fecha", return_value=True):
        assert exportador.exportar_parquet() == 0


def test_exportar_bolsa_end_to_end_e_idempotencia(mock_cargador_ibkr: CargarCarteraIBKR, tmp_path):
    """
    Test funcional completo con archivos reales temporales:
    1. Primera exportación de día 1 (2026-11-10): crea parquet particionado y devuelve 1.
    2. Segunda exportación idéntica (2026-11-10): detecta que existe y devuelve 0 (idempotente).
    3. Exportación de día 2 (2026-11-11): acumula ambos días sin borrar el anterior y devuelve 1.
    """
    ruta_parquet_temp = str(tmp_path / "bolsa_cartera.parquet")

    with patch("src.exportar_datos.RUTA_BOLSA_CARTERA", ruta_parquet_temp):
        exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")

        # 1. Primera exportación
        res1 = exportador.exportar_parquet()
        assert res1 == 1

        df_guardado = pd.read_parquet(ruta_parquet_temp)
        assert len(df_guardado) == 2
        assert list(df_guardado["fecha"].unique()) == [pd.Timestamp("2026-11-10")]
        assert list(df_guardado["año"].unique()) == [2026]

        # 2. Re-ejecutar el mismo día (idempotencia)
        res2 = exportador.exportar_parquet()
        assert res2 == 0

        df_despues = pd.read_parquet(ruta_parquet_temp)
        assert len(df_despues) == 2  # No se han duplicado las filas

        # 3. Exportar un día nuevo (2026-11-11)
        df_dia_2 = mock_cargador_ibkr.df.copy()
        df_dia_2["fecha"] = pd.to_datetime(["2026-11-11", "2026-11-11"])
        mock_cargador_dia2 = Mock(spec=CargarCarteraIBKR)
        mock_cargador_dia2.df = df_dia_2

        exportador_dia2 = ExportarDatos(mock_cargador_dia2, tipo="bolsa")
        res3 = exportador_dia2.exportar_parquet()
        assert res3 == 1

        df_total = pd.read_parquet(ruta_parquet_temp)
        assert len(df_total) == 4
        assert set(df_total["fecha"]) == {pd.Timestamp("2026-11-10"), pd.Timestamp("2026-11-11")}


# ============================================================================
# TESTS PARA validar_fecha Y tipo='bolsa'
# ============================================================================

@pytest.fixture
def mock_cargar_ibkr_df() -> pd.DataFrame:
    """Fixture con DataFrame procesado de cartera IBKR."""
    return pd.DataFrame({
        "fecha": pd.to_datetime(["2026-11-10", "2026-11-10"]),
        "symbol": ["IBE", "AAPL"],
        "description": ["IBERDROLA SA", "APPLE INC"],
        "currency": ["EUR", "USD"],
        "quantity": [10.0, 5.0],
        "mark_price": [20.0, 150.0],
        "cost_basis_price": [18.0, 140.0],
        "cost_basis_money": [180.0, 700.0],
        "position_value": [200.0, 750.0],
        "fifo_pnl_unrealized": [20.0, 50.0],
        "fx_rate_to_base": [1.0, 0.9],
        "cost_basis_eur": [180.0, 630.0],
        "position_value_eur": [200.0, 675.0],
        "unrealized_pnl_eur": [20.0, 45.0],
        "pnl_percent": [11.11, 7.14],
        "percent_of_nav": [50.0, 50.0],
        "año": [2026, 2026],
    })


@pytest.fixture
def mock_cargador_ibkr(mock_cargar_ibkr_df: pd.DataFrame) -> CargarCarteraIBKR:
    """Fixture que crea un mock de CargarCarteraIBKR."""
    mock = Mock(spec=CargarCarteraIBKR)
    mock.df = mock_cargar_ibkr_df
    return mock


def test_validar_fecha_file_not_found(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que si no existe bolsa_cartera.parquet, validar_fecha devuelve False."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    with patch("pandas.read_parquet", side_effect=FileNotFoundError()):
        assert exportador.validar_fecha() is False


def test_validar_fecha_date_exists(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que devuelva True si la fecha ya existe en el parquet."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    df_existente = pd.DataFrame({"fecha": pd.to_datetime(["2026-11-10", "2026-11-09"])})
    with patch("pandas.read_parquet", return_value=df_existente):
        assert exportador.validar_fecha() is True


def test_validar_fecha_date_not_exists(mock_cargador_ibkr: CargarCarteraIBKR):
    """Verifica que devuelva False si la fecha es nueva."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    df_existente = pd.DataFrame({"fecha": pd.to_datetime(["2026-11-09"])})
    with patch("pandas.read_parquet", return_value=df_existente):
        assert exportador.validar_fecha() is False


def test_exportar_bolsa_when_validation_true(mock_cargador_ibkr: CargarCarteraIBKR):
    """Si la fecha ya existe, exportar_parquet devuelve 0 y no exporta."""
    exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")
    with patch.object(exportador, "validar_fecha", return_value=True):
        assert exportador.exportar_parquet() == 0


def test_exportar_bolsa_end_to_end_e_idempotencia(mock_cargador_ibkr: CargarCarteraIBKR, tmp_path):
    """
    Test funcional completo con archivos reales temporales:
    1. Primera exportación de día 1 (2026-11-10): crea parquet particionado y devuelve 1.
    2. Segunda exportación idéntica (2026-11-10): detecta que existe y devuelve 0 (idempotente).
    3. Exportación de día 2 (2026-11-11): acumula ambos días sin borrar el anterior y devuelve 1.
    """
    ruta_parquet_temp = str(tmp_path / "bolsa_cartera.parquet")

    with patch("src.exportar_datos.RUTA_BOLSA_CARTERA", ruta_parquet_temp):
        exportador = ExportarDatos(mock_cargador_ibkr, tipo="bolsa")

        # 1. Primera exportación
        res1 = exportador.exportar_parquet()
        assert res1 == 1

        df_guardado = pd.read_parquet(ruta_parquet_temp)
        assert len(df_guardado) == 2
        assert list(df_guardado["fecha"].unique()) == [pd.Timestamp("2026-11-10")]
        assert list(df_guardado["año"].unique()) == [2026]

        # 2. Re-ejecutar el mismo día (idempotencia)
        res2 = exportador.exportar_parquet()
        assert res2 == 0

        df_despues = pd.read_parquet(ruta_parquet_temp)
        assert len(df_despues) == 2  # No se han duplicado las filas

        # 3. Exportar un día nuevo (2026-11-11)
        df_dia_2 = mock_cargador_ibkr.df.copy()
        df_dia_2["fecha"] = pd.to_datetime(["2026-11-11", "2026-11-11"])
        mock_cargador_dia2 = Mock(spec=CargarCarteraIBKR)
        mock_cargador_dia2.df = df_dia_2

        exportador_dia2 = ExportarDatos(mock_cargador_dia2, tipo="bolsa")
        res3 = exportador_dia2.exportar_parquet()
        assert res3 == 1

        df_total = pd.read_parquet(ruta_parquet_temp)
        assert len(df_total) == 4
        assert set(df_total["fecha"]) == {pd.Timestamp("2026-11-10"), pd.Timestamp("2026-11-11")}

