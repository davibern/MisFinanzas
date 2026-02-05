# Directorio raw/

Este directorio contiene los archivos XML fuente con los datos financieros originales.

## Fuente de datos

El fichero, si bien es ficticio para entender la estructura del mismo, está basado en el fichero oficial que se descarga de la aplicación de CaixaBank del apartado de clientes de finanzas (movimientos - gastos e ingresos).

Se fija la fecha de estudio, normalmente el mes pasado, de visualizan todos los movimientos del mes y se pulsa finalmente en descargar, seleccionando cuidadosamente que se incluyan todos los elementos de la pantalla para su exportación.

## Estructura de los archivos XML

Los archivos XML siguen el formato **Microsoft Excel XML Spreadsheet** (SpreadsheetML), que es un formato XML utilizado por Microsoft Excel para representar hojas de cálculo.

### Formato de nombres

Los archivos se nombran siguiendo el patrón `YYYYMM.xml`, donde:
- `YYYY` = Año (4 dígitos)
- `MM` = Mes (2 dígitos)

**Ejemplos:**
- `202401.xml` - Datos de enero de 2024
- `202512.xml` - Datos de diciembre de 2025

### Estructura del XML

Cada archivo XML contiene:

#### 1. Declaración y namespaces
```xml
<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" ...>
```

#### 2. Hoja de trabajo principal
El nombre de la hoja debe ser exactamente: **"Ingresos y Gastos"**

```xml
<Worksheet ss:Name="Ingresos y Gastos">
```

#### 3. Encabezados de columnas (Fila 1)
Las columnas deben aparecer en este orden:

| Columna | Nombre | Descripción |
|---------|--------|-------------|
| 1 | Fecha | Fecha de la transacción (formato: DD/MM/YYYY) |
| 2 | Concepto | Descripción de la transacción |
| 3 | Categoría | Categoría de la transacción |
| 4 | Importe (€) | Cantidad en euros (positivo para ingresos, negativo para gastos) |
| 5 | Tipo Movimiento | "Ingreso (I)" o "Gasto (G)" |
| 6 | Cuenta/Tarjeta | Cuenta o tarjeta utilizada |

#### 4. Filas de datos
Cada fila representa una transacción financiera:

```xml
<Row>
    <Cell ss:Index="2" ss:StyleID="s81">
        <Data ss:Type="String">15/01/2025</Data>
    </Cell>
    <Cell ss:StyleID="s81">
        <Data ss:Type="String">Salario mensual</Data>
    </Cell>
    <Cell ss:StyleID="s81">
        <Data ss:Type="String">Nómina</Data>
    </Cell>
    <Cell ss:StyleID="s84">
        <Data ss:Type="Number">2500.00</Data>
    </Cell>
    <Cell ss:StyleID="s81">
        <Data ss:Type="String">Ingreso (I)</Data>
    </Cell>
    <Cell ss:StyleID="s82">
        <Data ss:Type="String">Cuenta Corriente</Data>
    </Cell>
</Row>
```

### Tipos de datos

- **Fecha**: String en formato DD/MM/YYYY
- **Concepto**: String
- **Categoría**: String
- **Importe**: Number (decimal con punto como separador)
- **Tipo Movimiento**: String - "Ingreso (I)" o "Gasto (G)"
- **Cuenta/Tarjeta**: String

### Convenciones importantes

1. **Importes negativos**: Los gastos se representan con valores negativos (ej: -85.50)
2. **Importes positivos**: Los ingresos se representan con valores positivos (ej: 2500.00)
3. **Formato de fecha**: Siempre DD/MM/YYYY (ej: 15/01/2025)
4. **Tipo de movimiento**: Debe incluir el sufijo "(I)" para ingresos o "(G)" para gastos

### Procesamiento

El archivo [`src/cargar_fichero.py`](../src/cargar_fichero.py) se encarga de:

1. **Parsear el XML** usando lxml
2. **Extraer los datos** de la hoja "Ingresos y Gastos"
3. **Limpiar y transformar** los datos:
   - Convertir fechas a formato datetime
   - Convertir importes a float
   - Extraer el tipo simplificado (Ingreso/Gasto)
   - Añadir columnas calculadas (mes, año, mes_nombre, dia_semana)
4. **Exportar a Parquet** en el directorio `data/`

### Archivo de ejemplo

El archivo [`example.xml`](./example.xml) contiene 5 transacciones ficticias:
- 1 ingreso (Salario mensual)
- 4 gastos (Supermercado, Gasolina, Restaurante, Suscripción)

Este archivo puede usarse como plantilla para crear nuevos archivos de datos.

## Categorías comunes

Basándose en los datos existentes, estas son algunas categorías típicas:

**Ingresos:**
- Nómina / pensión / desempleo

**Gastos:**
- Alimentación / Supers e hipers
- Transporte
- Ocio / Restaurantes
- Servicios / Cuotas y suscripciones
- Hogar
- Salud
- Ropa y calzado
- Seguros y mutuas
- Gastos en hipotecas y préstamos
- Varios
- Dinero del cajero
- Transferencias realizadas
- Bizum realizado
