"""
Test unitario para la clase CargarCarteraIBKR

Este archivo contiene tests unitarios para validar el funcionamiento de:
- Inicialización y extracción de fecha a partir del nombre del fichero
- Lectura de ficheros CSV de Interactive Brokers
- Limpieza, renombrado y cálculo de métricas en EUR
- Manejo de excepciones cuando la fecha no es válida
"""

import pytest
import pandas as pd
from pathlib import Path
from src.cargar_datos_ibkr import CargarCarteraIBKR


@pytest.fixture
def csv_ibkr_content() -> str:
    """
    Fixture: Crea contenido CSV de ejemplo con valores en EUR y USD.
    """
    return (
        '"Symbol","Quantity","MarkPrice","PositionValue","CostBasisPrice","CostBasisMoney",'
        '"PercentOfNAV","FifoPnlUnrealized","CurrencyPrimary","FXRateToBase","Description"\n'
        '"IBE","10.0","20.0","200.0","18.0","180.0","50.0","20.0","EUR","1.0","IBERDROLA SA"\n'
        '"AAPL","5.0","150.0","750.0","140.0","700.0","50.0","50.0","USD","0.9","APPLE INC"\n'
    )


@pytest.fixture
def mock_csv_file(csv_ibkr_content: str, tmp_path: Path) -> Path:
    """
    Fixture: Crea un archivo CSV temporal con fecha en el nombre.
    """
    csv_file = tmp_path / "ibkr_cartera_operaciones_20261110.csv"
    csv_file.write_text(csv_ibkr_content, encoding="utf-8")
    return csv_file


# ============================================================================
# TESTS PARA __init__ Y EXTRACCIÓN DE FECHA
# ============================================================================

def test_init_cargar_cartera_ibkr(mock_csv_file: Path) -> None:
    cargador = CargarCarteraIBKR(str(mock_csv_file))
    assert cargador.fichero == str(mock_csv_file)
    assert cargador.df is None
    assert cargador.fecha == "20261110"


def test_extraer_fecha_sin_fecha(tmp_path: Path) -> None:
    archivo_sin_fecha = tmp_path / "cartera.csv"
    archivo_sin_fecha.write_text("dummy", encoding="utf-8")
    cargador = CargarCarteraIBKR(str(archivo_sin_fecha))
    assert cargador.fecha is None


# ============================================================================
# TESTS PARA leer_fichero Y limpiar_datos
# ============================================================================

def test_leer_fichero(mock_csv_file: Path) -> None:
    cargador = CargarCarteraIBKR(str(mock_csv_file))
    df = cargador.leer_fichero()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "Symbol" in df.columns


def test_limpiar_datos_error_sin_fecha(tmp_path: Path) -> None:
    archivo_sin_fecha = tmp_path / "cartera.csv"
    archivo_sin_fecha.write_text("dummy", encoding="utf-8")
    cargador = CargarCarteraIBKR(str(archivo_sin_fecha))

    with pytest.raises(ValueError) as excinfo:
        cargador.limpiar_datos()

    assert "No se pudo extraer la fecha" in str(excinfo.value)


def test_limpiar_datos_esquema_y_calculos(mock_csv_file: Path) -> None:
    cargador = CargarCarteraIBKR(str(mock_csv_file))
    df = cargador.limpiar_datos()

    # 1. Esquema y orden exacto de columnas
    assert list(df.columns) == CargarCarteraIBKR.ESQUEMA_COLUMNAS
    assert len(df) == 2

    # 2. Fecha y año
    assert df["fecha"].iloc[0] == pd.Timestamp("2026-11-10")
    assert df["año"].iloc[0] == 2026

    # 3. Posición en EUR (IBE - FX rate 1.0)
    ibe = df[df["symbol"] == "IBE"].iloc[0]
    assert ibe["cost_basis_eur"] == 180.0
    assert ibe["position_value_eur"] == 200.0
    assert ibe["unrealized_pnl_eur"] == 20.0
    assert ibe["pnl_percent"] == round((20.0 / 180.0) * 100, 4)

    # 4. Posición en USD (AAPL - FX rate 0.9)
    aapl = df[df["symbol"] == "AAPL"].iloc[0]
    assert aapl["cost_basis_eur"] == round(700.0 * 0.9, 4)
    assert aapl["position_value_eur"] == round(750.0 * 0.9, 4)
    assert aapl["unrealized_pnl_eur"] == round(50.0 * 0.9, 4)
    assert aapl["pnl_percent"] == round((50.0 / 700.0) * 100, 4)


def test_limpiar_datos_cost_basis_zero(tmp_path: Path) -> None:
    """Verifica que si cost_basis_money es 0, no falle por división por cero y devuelva 0.0."""
    csv_zero = (
        '"Symbol","Quantity","MarkPrice","PositionValue","CostBasisPrice","CostBasisMoney",'
        '"PercentOfNAV","FifoPnlUnrealized","CurrencyPrimary","FXRateToBase","Description"\n'
        '"CASH","1.0","0.0","0.0","0.0","0.0","0.0","0.0","EUR","1.0","CASH ITEM"\n'
    )
    archivo = tmp_path / "ibkr_cartera_operaciones_20261110.csv"
    archivo.write_text(csv_zero, encoding="utf-8")

    cargador = CargarCarteraIBKR(str(archivo))
    df = cargador.limpiar_datos()

    assert df["pnl_percent"].iloc[0] == 0.0
