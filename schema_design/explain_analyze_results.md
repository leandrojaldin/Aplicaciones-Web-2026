# Resultados de EXPLAIN ANALYZE

## Comparación de Rendimiento en la tabla `clientes`

### 1. Sin Índice (Seq Scan)
* **Tiempo de ejecución:** 7.526 ms
* **¿Por qué tardó más?** Sin el índice, la base de datos tuvo que realizar un escaneo secuencial (`Seq Scan`), lo que significa que revisó los 100,000 registros de la tabla uno por uno desde el principio hasta el final para encontrar los que coincidían con la fecha.

### 2. Con Índice (Bitmap Index Scan / Index Scan)
* **Tiempo de ejecución:** 1.110 ms
* **¿Por qué tardó menos?** Con el índice creado, la base de datos no necesitó revisar toda la tabla. El índice actuó como un "índice de un libro", permitiéndole saltar de forma directa y casi instantánea a la ubicación exacta de los datos buscados.

## Conclusión Final
* **Comparativa:** Sin índice tardó **7.526 ms** y con índice tardó **1.110 ms**.
* **Motivo:** Se observa claramente que el uso del índice optimiza de forma notable la búsqueda. Tardó más al principio porque el motor se vio obligado a procesar toda la tabla fila por fila, y tardó menos después porque el índice redujo el esfuerzo de búsqueda al ubicar la información de forma directa.