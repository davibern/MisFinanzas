from pathlib import Path

# Rutas base relativas al proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = BASE_DIR / "raw"

# Rutas específicas para constantes
RUTA_FINANZAS_PARQUET = str(DATA_DIR / "finanzas.parquet")
RUTA_AHORROS_PARQUET = str(DATA_DIR / "ahorros.parquet")
