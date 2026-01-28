# CONTROL DE CAMBIOS

## [0.0.4] - 2026-01-28
### Modificado
- Refactorizar el código de `app.py` para mejorar la legibilidad y organización.
- Mejorar la información mostrada en la página `cargar_datos.py`.
- Mejorar el tamaño de la imagen en la página de inicio, `assets/logo.png`.

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