# CONTROL DE CAMBIOS

## [0.0.8] - 2026-02-02
### Añadido
- Añadir ficheros de tests para MisFinanzas.
### Modificado
- Añadir dependencia para realizar tests con pytest.    

## [0.0.7] - 2026-02-02
### Modificado
- Eliminación del campo de filtro del mes en la página `datos_por_meses.py`.
- Eliminar el fichero `main.py`.

## [0.0.6] - 2026-01-31
### Añadido
- Texto introductorio en la página `datos_por_mes.py` explicando las funcionalidades disponibles.
- Nueva página `datos_por_meses.py` para mostrar gráficos de barras con la evolución de ingresos y gastos mensuales a lo largo del año.
### Modificado
- Corrección del cálculo del delta de ingresos y gastos en `datos_por_mes.py` cuando el mes es enero, para obtener correctamente los datos del mes anterior (diciembre del año anterior).
- Correción del formato de `datos_por_mes.py` para eliminar líneas en blanco innecesarias.
- Cambiado icono de resumen mensual en `app.py` a `:material/stacked_bar_chart:` para mayor claridad.
- Corregido formato en `app.py`.

## [0.0.5] - 2026-01-29
### Añadido
- Implementar funcionalidad en `datos_por_mes.py` para mostrar tarjetas de estadísticas del total de gastos, ingresos y diferencia del mes y su comparativa con el mes anterior.
- Añadir configuración general de la app para ocultar el botón Deploy.
### Modificado
- Actualización de comentarios en `datos_por_mes.py`.

## [0.0.4] - 2026-01-28
### Añadido
- Implementar librería Plotly para crear gráficos interactivos.
- Implementar funcionalidad en `datos_por_mes.py` para mostrar gráficos de barras de los gastos por categoría.
### Modificado
- Refactorizar el código de `app.py` para mejorar la legibilidad y organización.
- Mejorar la información mostrada en la página `cargar_datos.py`.
- Mejorar el tamaño de la imagen en la página de inicio, `assets/logo.png`.
- Actualización de dependencias en el archivo `requirements.txt` para incluir Plotly.

## [0.0.3] - 2025-01-27
### Añadido
- Implementar librería Streamlit para crear una interfaz web para consumir los datos.
- Implementar funcionalidad en `cargar_datos.py` para cargar datos desde la interfaz web.
- Añadir imagen central para la página de inicio.
### Modificado
- Actualización de dependencias en el archivo `requirements.txt` para incluir Streamlit y eliminar pandas (al venir preinstalado con Streamlit).
- Cambiar funcionalidad de `exportar` en `src/exportar_datos.py` para que devuelva un número indicando éxito o fallo. 0 para fallo y 1 para éxito.

## [0.0.2] - 2025-01-25
### Añadido
- Nueva funcionalidad para obtener ingresos agrupados por categoría en un mes y año específicos.
- Nueva funcionalidad para obtener gastos agrupados por categoría en un mes y año específicos.
### Modificado
- Actualización de los ejemplos en `main.py` para reflejar las nuevas funcionalidades añadidas.
- Corrección de nombre en el DataFrame exportado evitando caracteres especiales.

## [0.0.1] - 2025-01-23
### Añadido
- Inicio del proyecto Mis Finanzas para la gestión personal de gastos e ingresos.
    - Funcionalidades para cargar datos desde archivos XML.
    - Exportación de datos a formato Parquet.
    - Cálculo de ingresos y gastos mensuales y anuales.