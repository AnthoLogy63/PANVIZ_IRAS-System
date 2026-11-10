# Requisitos B0 y cambio CR01 · versión 1.0

Fuente: trab_81.pdf, sección 2. Alcance aprobado por la instrucción del usuario: aplicación local completa y persistencia SQLite. Aprobación académica B0: pendiente de E1/E2; no equivale a la autorización de implementación del usuario.

| ID | Descripción | Criterio de aceptación | Responsable | Versión |
|---|---|---|---|---|
| R01 | Importar id, fecha_notificacion, establecimiento, distrito, grupo_etario, evento | CSV inicial sobre BD vacía produce 20 filas evaluadas; muestra vista previa y conserva aceptadas al confirmar | E2 | B0 |
| R02 | Rechazar datos incompletos, fechas imposibles y duplicados; registrar fila/motivo | 15 válidas sin falsos rechazos y 5 inválidas detectadas; líneas 17–21 | E2 | B0 |
| R03 | Consolidar por semana ISO, establecimiento, distrito y edad | 15 grupos iniciales, total 15; año ISO correcto en cambio de año | E2 | B0 |
| R04 | Exportar y reconciliar | CSV con encabezados definidos; suma total igual al número de aceptados dentro de los mismos filtros | E2 | B0 |
| R05 | Trazar requisito, cambio, código, prueba y versión | Matriz cubre R01–R05 y CR01; registros identifican versión, autor y revisor reales antes de B2 | E5 | B0/v0.1 |
| CR01 | Filtrar consolidado por distrito | Ate muestra/exporta 5 aceptadas; distrito inexistente devuelve 0; limpiar devuelve 15; no altera BD | E2 | v0.1 |

No funcionales: Python >=3.10; Flask único; SQLite con sqlite3 de biblioteca estándar; interfaz en español; diseño adaptable; accesibilidad por teclado; ejecución local reproducible; ningún dato personal real.

Política de carga: la primera ejecución carga el conjunto sintético de demostración una sola vez. Cada carga posterior crea un lote inmutable. Un ID aceptado no puede repetirse, incluso cambiando mayúsculas; un ID rechazado puede corregirse y volverse a cargar. La segunda importación idéntica produce 0 aceptados y 20 rechazos.
