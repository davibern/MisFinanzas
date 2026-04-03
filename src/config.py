from pathlib import Path

# Rutas base relativas al proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = BASE_DIR / "raw"

# Rutas específicas para constantes
RUTA_FINANZAS_PARQUET = str(DATA_DIR / "finanzas.parquet")
RUTA_AHORROS_PARQUET = str(DATA_DIR / "ahorros.parquet")
RUTA_CAJA_PARQUET = str(DATA_DIR / "caja.parquet")


class Color:
    """Clase para guardar los colores de la aplicación"""
    AZUL = "#1f77b4"
    NARANJA = "#ff7f0e"
    VERDE = "#2ca02c"
    ROJO = "#d62728"
    MORADO = "#9467bd"
    MARRON = "#8c564b"
    ROSA = "#e377c2"
    GRIS = "#7f7f7f"
    OLIVA = "#bcbd22"
    CIAN = "#17becf"
