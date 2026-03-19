# CONTROL DE CAMBIOS

## [0.0.35] - 2026-03-19
### Añadido
- Añadir delta de ahorro en `pages/ahorro_prevision.py`
### Modificado
- Corregir texto literal de la ayuda de carga de datos de ahorro.

## [0.0.34] - 2026-03-17
### Añadido
- Añadir tests para los métodos de gráficos de ahorros

## [0.0.33] - 2026-03-15
### Añadido
- Añadir aviso al usuario de que no hay datos de ahorro sino se encuentran ficheros con datos de ahorro.
- Añadir métodos en `mis_ahorros.py` para calcular el total aportado a un plan de ahorro y el acumulado.
- Mostra datos acumulados totales (aportado y acumulado) en `ahorro_prevision.py`

## [0.0.32] - 2026-03-12
### Modificado
- Eliminar `Forward-Fill` en la carga de datos de ahorro para que se muestren los datos correctamente en las gráficas e impedir que se infiera información "duplicada".
- Conectar los puntos de las gráficas de ahorro para que se muestren de manera continua.
- Añadir pestañas en ahorro para diferenciar los planes de ahorro.
- Añadir breves descripciones de los indicadores de ahorro.
### Corregido
- Corregido los tests de carga y exportación de ahorros.
- Corregido texto literal de la ayuda de carga de datos de ahorro.

## [0.0.31] - 2026-03-10
### Añadido
- Añadir métodos para graficar ahorros de axa y fiatc
- Añadir gráficos de ahorros de axa y fiatc
- Añadir tests para los métodos de gráficos de ahorros
### Modificado
- Cambiar nombre de variables en la parte de ahorro para que sea más legible y mantenible

## [0.0.30] - 2026-03-09
### Añadido
- Limpiar caché cuando se añaden datos de ahorros.
- Crear clase inicial para obtener estadísticas de ahorro
- Crear tests iniciales para los datos estadísticos de ahorros

## [0.0.29] - 2026-03-07
### Añadido
- Cuando se importa los datos de ahorro, se guarda el fichero como copia de seguridad en `raw` con el mismo formato orignal.
- Se añade página de ayuda para la carga de datos de ahorro.
- Se añade navegación para la ayuda de cargar datos de ahorro.
- Tests unitarios para cargar datos de ahorro.
### Modificado
- Se corrige texto literal de la ayuda de carga de datos bancarios.
- Se corrige texto literal de la ayuda de carga de datos de ahorro.

## [0.0.28] - 2026-03-04
### Añadido
- Nueva columna de total acumulado para poder calcular beneficio/pérdida.
- Información de si la carga del dato se ha realizado correctamente.
### Modificado
- Validar que la carpeta /src está creada y si no la crea para evitar errores FileNotFoundError o NotADirectoryError.

## [0.0.27] - 2026-03-03
### Añadido
- Nueva función para obtener el nombre de la compañía del fichero de ahorro.
### Modificado
- Cambiar la forma de eliminar el fichero de ahorro para que funcione con cualquier nombre de fichero.

## [0.0.26] - 2026-03-02
### Añadido
- Nueva función para exportar los datos de ahorro según compañía
### Modificado
- Cambiado los nombres de las clases de carga de datos y exportacion para que sea más legible y mantenible

## [0.0.25] - 2026-03-01
### Añadido
- Añadida nueva página `cargar_ahorro.py` para cargar los datos de ahorro previsión.
- Añadida nueva clase `CargarDatosAhorros` en `src/cargar_datos_ahorros.py` para procesar los datos de ahorro previsión.
- Añadida nueva opción de menú para cargar los datos de ahorro previsión en `app.py`.
### Modificado
- Corregido nombres y espacios de formato

## [0.0.24] - 2026-02-28
### Añadido
- Fichero de datos para los datos de inversión de AXA, con el mismo formato que el de FIATC.
- Fichero de ejemplo para los datos de invesión de AXA.
### Modificado
- Actualizar el README para incluir la información de los datos de inversión, con su correspondiente fichero de ejemplo.
- Renombrado el fichero de clase `CargarFichero` por el de `CargarFicheroBancario` para diferenciarlo del específico de carga de datos de ahorro.
- Renombrar el fichero `cargar_datos.py` por el de `cargar_datos_bancarios.py` para diferenciarlo del específico de carga de datos de ahorro.
- Eliminar librerías sin uso en los ficheros de tests.
- Mejorar el formato de los ficheros de tests.

## [0.0.23] - 2026-02-26
### Modificado
- Cambiar la ruta de los ficheros que se almacenan en `raw` para organizarlos por tipo: el bancario, y los de ahorro previsión.
- Actualizar el `.gitignore` para que no se almacenen los ficheros de producción..
- Crear un fichero de ejemplo para los datos de ahorro de FIATC.
- Actualizar el README para estructurar la información de manera más clara, especificando por un lado el fichero de ejemplo de los datos bancarios y por otro el de ahorro.

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