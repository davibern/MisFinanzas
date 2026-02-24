# CONTROL DE CAMBIOS

## [0.0.22] - 2026-02-25
### Modificado
- Mejorar la gráfica para mostrar el ahorro mensual en la página `ahorro_prevision.py`.
- Adaptar test al nuevo cambio agrupado por mes y tipo del ahorro.
- Cambiar método de obtención de datos para que traiga los datos separados por tipo de ahorro.

## [0.0.21] - 2026-02-23
### Añadido
- Añadida gráfica provisional para mostrar el ahorro mensual en la página `ahorro_prevision.py`.
- Añadido test unitario para la función `obtener_ahorro_jubilacion_por_meses` en `tests/test_mis_finanzas.py`.
- Añadido método `obtener_ahorro_jubilacion_por_meses` en `src/mis_finanzas.py` para obtener el ahorro diferido por jubilación mensual en un año.
### Modificado
- Cambiar el literal y las referencias de ahorro en la página `ahorro_prevision.py`.

## [0.0.20] - 2026-02-22
### Corregido
- Corrección de error al limpiar caché. No estaba llamando bien a la función.

## [0.0.19] - 2026-02-21
### Añadido
- Añadido enlace a la página de ayuda para exportar datos de CaixaBank en la página `cargar_datos.py`.

## [0.0.18] - 2026-02-20
### Añadido
- Mejorado los textos de ayuda al usuario y los campos de selección de fechas en `resumen_mensual.py` y `resumen_anual.py`.

## [0.0.17] - 2026-02-18
### Modificado
- Mejorar la información de los textos de ayuda en la página `cargar_datos.py` para que el usuario sepa qué formato debe seguir el nombre del archivo.
- Cambiar la distribución de los campos en `cargar_datos.py` para que no ocupen todo el año de pantalla con columnas.

## [0.0.16] - 2026-02-14
### Modificado
- Añadida caché de datos para mejorar el rendimiento en la carga de datos, carga de clasae y métodos. En `src/mis_finanzas.py` se ha añadido la caché de datos para mejorar el rendimiento en la carga de datos, carga de clasae y métodos. En `pages/cargar_datos.py` se ha añadido la caché de datos para mejorar el rendimiento en la carga de datos, carga de clasae y métodos.
- Limpiar caché de datos justo cuando se cargen nuevos para actualizar los datos almacenados.
### Añadido
- Añadido mensaje informativo en la página `cargar_datos.py` para informar al usuario de que los nuevos datos estarán disponibles al navegar a otras páginas.


## [0.0.15] - 2026-02-11
### Añadido
- Añadido gráfico de burbujas para mostrar el top 5 de gastos del mes en `/pages/resumen_mensual.py`

## [0.0.14] - 2026-02-10
### Añadido
- Añadida función para calcular el gasto medio diario del mes correspondiente. La función se llama `obtener_media_gastos_mes_año` y se encuentra en `src/mis_finanzas.py`. Esta función filtra los gastos del mes y año correspondientes, agrupa por fecha sumando los gastos de cada día (uso `abs()` para convertir los gastos a positivos) y luego calculo la media arimética de la suma de los gastos diarios.
- Se realiza el correspondiente test unitario para comprobar el correcto funcionamiento de la función, en `/tests/test_mis_finanzas.py`, y la función `test_obtener_media_gastos_mes_año`.
- Se añade una columna más en el fichero `resumen_mensual.py` para mostrar el gasto medio diario y el delta del mes anterior.

## [0.0.13] - 2026-02-09
### Añadido
- Añadida los tests para la función `cargar_datos` en `test_mis_finanzas.py`.
- Añadida los tests para la función `exportar_datos` en `test_mis_finanzas.py`.

## [0.0.12] - 2026-02-08
### Modificado
- Añadir validación para el nombre del archivo en la página `cargar_datos.py` para asegurar que siga el formato establecido, que es `YYYYMM`, y mostrar avisos al usuario en caso de que escriba mal el dato. No se motrará el componente de subida de archivos hasta que el nombre no sea correcto.
### Corregido
- Corrección de error cuando se selecciona un mes sin datos en la página `resumen_mensual.py`, mostrando al usuario información en lugar del código de error.

## [0.0.11] - 2026-02-07
### Añadido
- Añadida nueva organización de la información usando pestañas (`st.tabs`) en las páginas `resumen_mensual.py` y `ahorro.py` para mejorar la experiencia de usuario.

## [0.0.10] - 2026-02-05
### Añadido
- Añadidos los ficheros de ejemplos, tanto el fichero fuente que se descarga del área de cliente de CaixaBank como el parquet que se exporta al finalizar el proceso de importación. Estos ficheros se encuentran en `raw/example.xml` y `data/finanzas.parquet.example` respectivamente.
- Añadido nuevos indicadores en `ahorro.py` para mostrar el ahorro total acumulado a lo largo del año y la tasa de ahorro promedio mensual en el año de estudio.

## [0.0.9] - 2026-02-04
### Añadido
- Añadida página `/pages/ahorro.py` para mostrar la evolución del gasto-ingreso a lo largo de un año.
### Modificado
- Corrección de errores tipográficos en los comentarios del código.
- Añadido tipado en el retorno de las funciones de los tests en `test_mis_finanzas.py`.
- Añadido que salga automáticamente el año actual en el selector de años en la página `resumen_anual.py`.

## [0.0.8] - 2026-02-02
### Añadido
- Añadir ficheros de tests para MisFinanzas.
### Modificado
- Añadir dependencia para realizar tests con pytest.    

## [0.0.7] - 2026-02-02
### Modificado
- Eliminación del campo de filtro del mes en la página `resumen_anual.py`.
- Eliminar el fichero `main.py`.

## [0.0.6] - 2026-01-31
### Añadido
- Texto introductorio en la página `resumen_mensual.py` explicando las funcionalidades disponibles.
- Nueva página `resumen_anual.py` para mostrar gráficos de barras con la evolución de ingresos y gastos mensuales a lo largo del año.
### Modificado
- Corrección del cálculo del delta de ingresos y gastos en `resumen_mensual.py` cuando el mes es enero, para obtener correctamente los datos del mes anterior (diciembre del año anterior).
- Correción del formato de `resumen_mensual.py` para eliminar líneas en blanco innecesarias.
- Cambiado icono de resumen mensual en `app.py` a `:material/stacked_bar_chart:` para mayor claridad.
- Corregido formato en `app.py`.

## [0.0.5] - 2026-01-29
### Añadido
- Implementar funcionalidad en `resumen_mensual.py` para mostrar tarjetas de estadísticas del total de gastos, ingresos y diferencia del mes y su comparativa con el mes anterior.
- Añadir configuración general de la app para ocultar el botón Deploy.
### Modificado
- Actualización de comentarios en `resumen_mensual.py`.

## [0.0.4] - 2026-01-28
### Añadido
- Implementar librería Plotly para crear gráficos interactivos.
- Implementar funcionalidad en `resumen_mensual.py` para mostrar gráficos de barras de los gastos por categoría.
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