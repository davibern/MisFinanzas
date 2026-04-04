# Directorio raw/

Este directorio contiene los archivos fuente con los datos financieros originales, organizados por fuente de datos.

```
raw/
├── bancario/   → Movimientos bancarios exportados desde CaixaBank (formato XML)
├── caja/       → Flujo de caja mensual exportado desde hoja de cálculo (formato CSV)
├── fiatc/      → Control de inversiones exportado desde FIATC (formato CSV)
└── axa/        → Control de inversiones exportado desde AXA (formato CSV)
```

---

## bancario/

### Fuente de datos

Los ficheros XML se descargan desde la aplicación de CaixaBank, en el apartado de clientes de finanzas (movimientos - gastos e ingresos). Se fija el mes a estudiar, se visualizan todos los movimientos y se pulsa en descargar, seleccionando que se incluyan todos los elementos de la pantalla.

### Formato de nombres

Los archivos se nombran siguiendo el patrón `YYYYMM.xml`:
- `YYYY` = Año (4 dígitos)
- `MM` = Mes (2 dígitos)

**Ejemplos:** `202401.xml` (enero 2024), `202512.xml` (diciembre 2025)

### Estructura del XML

Los archivos siguen el formato **Microsoft Excel XML Spreadsheet** (SpreadsheetML). La hoja de trabajo debe llamarse exactamente **"Ingresos y Gastos"**.

#### Columnas

| Columna | Nombre | Descripción |
|---------|--------|-------------|
| 1 | Fecha | Fecha de la transacción (DD/MM/YYYY) |
| 2 | Concepto | Descripción de la transacción |
| 3 | Categoría | Categoría de la transacción |
| 4 | Importe (€) | Cantidad en euros (positivo = ingreso, negativo = gasto) |
| 5 | Tipo Movimiento | `Ingreso (I)` o `Gasto (G)` |
| 6 | Cuenta/Tarjeta | Cuenta o tarjeta utilizada |

#### Convenciones

1. **Importes negativos**: Gastos (ej: `-85.50`)
2. **Importes positivos**: Ingresos (ej: `2500.00`)
3. **Formato de fecha**: Siempre `DD/MM/YYYY`
4. **Tipo de movimiento**: Debe incluir el sufijo `(I)` o `(G)`

### Procesamiento

El archivo [`src/cargar_fichero.py`](../src/cargar_fichero.py) se encarga de:

1. **Parsear el XML** usando lxml
2. **Extraer los datos** de la hoja "Ingresos y Gastos"
3. **Limpiar y transformar** los datos (fechas, importes, tipo de movimiento, columnas calculadas)
4. **Exportar a Parquet** en el directorio `data/`

### Archivo de ejemplo

[`bancario/example.xml`](./bancario/example.xml) — 5 transacciones ficticias (1 ingreso + 4 gastos). Úsalo como plantilla de referencia.

### Categorías comunes

**Ingresos:** Nómina / pensión / desempleo

**Gastos:** Alimentación · Supers e hipers · Transporte · Ocio · Restaurantes · Servicios · Cuotas y suscripciones · Hogar · Salud · Ropa y calzado · Seguros y mutuas · Hipotecas y préstamos · Varios · Cajero · Transferencias · Bizum

---

## fiatc/ y axa/

### Fuente de datos

El fichero CSV se descarga desde los portales de clientes de:

- FIATC Seguros (plan de ahorro)
- AXA Seguros (plan de inversión)

### Formato de nombres

Los archivos exportados por FIATC se llaman:

```
- Control de Inversiones - FIATC.csv
- Control de Inversiones - AXA.csv
```

### Estructura del CSV

Los ficheros usan **coma** como separador de campos y **codificación UTF-8**.

#### Columnas

| Columna | Descripción |
|---------|-------------|
| `FECHA` | Fecha del movimiento en formato `DD/MM/AAAA` |
| `MOVIMIENTO` | Tipo de operación (ver valores posibles abajo) |
| `IMPORTE` | Importe del movimiento en euros (ej: `"50,00€"`) |
| `SALDO` | Saldo acumulado en euros — solo se informa en `APORTACIÓN INICIAL` y `SALDO INICIO PERIODO`; vacío en el resto |

#### Valores posibles del campo MOVIMIENTO

| Valor | Descripción |
|-------|-------------|
| `APORTACIÓN INICIAL` | Primera aportación al plan |
| `APORTACIÓN PERIÓDICA` | Aportación mensual recurrente |
| `SALDO INICIO PERIODO` | Balance acumulado al cierre de cada trimestre |

#### Convenciones

1. **Importes**: Siempre positivos. Los valores usan coma decimal y símbolo `€` (ej: `"50,00€"`)
2. **Saldo**: Solo aparece relleno en la primera fila y en las filas de cierre trimestral
3. **Frecuencia**: Las aportaciones periódicas son mensuales; los cierres de periodo son trimestrales

### Procesamiento

El archivo [`src/cargar_fichero.py`](../src/cargar_fichero.py) se encarga de:

1. **Leer el CSV** ignorando las líneas de comentario iniciales
2. **Limpiar los importes**: eliminar el símbolo `€` y convertir la coma decimal a punto
3. **Transformar los datos**: convertir fechas, filtrar por tipo de movimiento
4. **Integrar con el resto** de datos financieros para el cálculo del ahorro

### Archivo de ejemplo

[`fiatc/example.csv`](./fiatc/example.csv) — 8 filas ficticias que cubren 2 trimestres completos (aportación inicial + aportaciones periódicas + cierres trimestrales). Úsalo como plantilla de referencia.

---

## caja/

### Fuente de datos

El fichero CSV se exporta desde una hoja de cálculo de seguimiento del flujo de caja familiar (p. ej. Google Sheets o Excel). Cada fila representa el saldo de caja registrado en una fecha concreta.

### Formato de nombres

El archivo exportado se llama:

```
Economía Familiar - Flujo de caja.csv
```

### Estructura del CSV

El fichero usa **coma** como separador de campos y **codificación UTF-8**.

#### Columnas

| Columna | Descripción |
|---------|-------------|
| `FECHA` | Fecha del registro en formato `DD/MM/AAAA` |
| `CAJA` | Saldo de caja en euros (ej: `"€10.891,38"`) |

#### Convenciones

1. **Importes**: Siempre positivos. Los valores usan punto como separador de miles, coma decimal y símbolo `€` como prefijo (ej: `"€10.891,38"`)
2. **Fecha**: Una entrada por mes, habitualmente el día de liquidación mensual
3. **Codificación**: UTF-8 (el nombre del fichero contiene caracteres especiales)

### Procesamiento

El archivo [`src/cargar_datos_caja.py`](../src/cargar_datos_caja.py) se encarga de:

1. **Leer el CSV** con `pandas.read_csv`
2. **Limpiar los importes**: eliminar el símbolo `€`, los puntos de miles y convertir la coma decimal a punto
3. **Transformar las fechas**: parsear con `dayfirst=True` y rellenar huecos hacia adelante (`ffill`)
4. **Exportar a Parquet** en el directorio `data/`

### Archivo de ejemplo

[`caja/example.csv`](./caja/example.csv) — Filas ficticias con la estructura esperada por `CargarFicheroCaja`. Úsalo como plantilla de referencia.