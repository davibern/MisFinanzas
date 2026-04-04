# Mis Finanzas

Aplicación interactiva desarrollada en **Python** utilizando el framework [Streamlit](https://github.com/streamlit/streamlit) para la gestión exhaustiva y visual de las finanzas personales.

## Objetivo

El objetivo principal de la aplicación es consolidar la información financiera procedente de distintas fuentes (cuentas bancarias, ahorros y efectivo o caja) para ofrecer un resumen detallado y visual que facilite el análisis y la toma de decisiones económicas.

## Características y Opciones de la Aplicación

La aplicación está organizada en diferentes secciones para facilitar su uso:

### 🏠 Inicio
Pantalla principal de bienvenida a la aplicación.

### 📊 Informes
- **Resumen Mensual:** Análisis detallado de los ingresos y gastos mes a mes.
- **Resumen Anual:** Perspectiva general e indicadores clave agrupados por año.
- **Ahorro y Previsión:** Seguimiento del estado actual de los ahorros y proyecciones a futuro.

### 🛠️ Herramientas
- **Cargar Banco:** Importa y procesa los movimientos bancarios.
- **Cargar Ahorro:** Carga e integra los datos de los depósitos o planes de ahorro.
- **Cargar Caja:** Registro y actualización del flujo de efectivo o caja.

### ❓ Ayuda
Secciones de consulta con información relevante sobre el formato y la estructura esperada para cada tipo de dato a importar:
- **Ayuda datos bancarios:** Instrucciones para los archivos de movimientos bancarios.
- **Ayuda datos ahorro:** Instrucciones para los datos de ahorro aportados.
- **Ayuda datos flujo de caja:** Instrucciones para el registro de movimientos en caja.

## Instrucciones de Instalación Local

Para ejecutar este proyecto en tu máquina local, sigue estos pasos recomendados utilizando un entorno virtual.

### 1. Clonar el repositorio
Si aún no lo has hecho, clona el proyecto y entra en su directorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd MisFinanzas
```

### 2. Crear y activar un entorno virtual
Se recomienda el uso de un entorno virtual para aislar las dependencias del proyecto. Crea y activa el entorno según tu sistema operativo:

**En Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias
Una vez que el entorno virtual esté activado (verás un `(.venv)` en la línea de comandos), instala las librerías requeridas incluidas en el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación
Para comenzar a utilizar la aplicación localmente, inicia el servidor de Streamlit usando el siguiente comando:
```bash
streamlit run app.py
```
Tras ejecutar este comando, la aplicación se abrirá automáticamente en una nueva pestaña de tu navegador web predeterminado (por lo general en `http://localhost:8501`).

## Capturas de Pantalla

> Las capturas de pantalla muestran datos de ejemplo, no son datos reales.

### Inicio
![Inicio](assets/demo/pantalla_inicio.png)

### Pantalla de resumen mensual
![Pantalla de resumen mensual](assets/demo/pantalla_resumen_mensual_1.png)
![Pantalla de resumen mensual](assets/demo/pantalla_resumen_mensual_2.png)

### Pantalla de carga de datos
![Pantalla de carga de datos](assets/demo/pantalla_carga_datos.png)