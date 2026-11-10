# Diseño técnico · 1.0

Una aplicación Flask con factory create_app, cuatro Blueprints y Jinja2. No hay servidor frontend. Tailwind precompilado complementa el sistema visual local; Chart.js presenta agregados calculados en SQLite/Python. Los gráficos tienen datos tabulados alternativos. JavaScript mejora navegación, búsqueda, orden y arrastrar archivos; la validación definitiva es de servidor.

Flujo: archivo -> contrato CSV -> validación de filas -> vista previa en SQLite vinculada a sesión -> confirmación -> BEGIN IMMEDIATE -> revalidación contra IDs actuales -> inserción del lote, aceptadas y rechazadas -> COMMIT -> consolidación -> reconciliación -> CSV. Si hay error de escritura, el lote completo se revierte. Una vista previa vence después de una hora y se usa una sola vez. El token secreto no viaja en la URL.

| Tabla | Contenido / integridad |
|---|---|
| batches | archivo, fecha UTC, origen, contadores aceptados/rechazados |
| notifications | id PRIMARY KEY COLLATE NOCASE, seis campos, semana_iso y FK al lote |
| rejections | FK al lote, fila, id recibido, motivo, JSON normalizado y distrito |
| previews | token aleatorio, archivo, bytes CSV y fecha UTC; sin datos en cookie |

SQLite se conecta por contexto Flask, activa foreign_keys y espera hasta 15 segundos por bloqueo. El esquema usa user_version=1. La base es local y no requiere ORM ni migrador para este primer esquema. El entorno inicializa tablas con CREATE IF NOT EXISTS. Un cambio de esquema futuro necesitará migración versionada antes de modificar user_version.

Consultas de filtros con valores parametrizados; nombres de columnas desde lista cerrada. Jinja escapa datos; JSON gráfico usa tojson. Formularios con CSRF, cookies HttpOnly/SameSite y límites de carga. Las celdas CSV que pueden interpretarse como fórmulas reciben un apóstrofo. Sin autenticación porque está fuera de alcance; host local y debug desactivado.

| Interfaz | Método | Resultado |
|---|---|---|
| / | GET | dashboard y filtros |
| /importacion/ | GET/POST | carga y vista previa |
| /importacion/confirmar | POST | transacción e informe del lote |
| /importacion/ejemplo.csv | GET | descarga del conjunto sintético |
| /validacion/ | GET | rechazos por lote/distrito |
| /reportes/ | GET | grupos, filtros y reconciliación |
| /reportes/consolidado.csv | GET | exportación con los filtros de la pantalla |
| /reportes/rechazos.csv | GET | exportación con lote/distrito |

Pruebas: reglas aisladas + integración real con cliente Flask y SQLite temporal. Ninguna prueba modifica instance/. Los resultados de ejecución deben incorporarse con scripts/verificar.py y el acta de validación.
