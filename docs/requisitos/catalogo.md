# Contrato CSV y supuestos · 1.0

Columnas obligatorias exactas, en cualquier orden: id, fecha_notificacion, establecimiento, distrito, grupo_etario, evento. Los encabezados ignoran espacios exteriores, mayúsculas y tildes; fecha_notificación se normaliza a fecha_notificacion. No se aceptan columnas adicionales ni repetidas. Delimitador coma o punto y coma, elegido a partir del encabezado. UTF-8 con BOM opcional. Líneas vacías se omiten; un archivo sin registros es inválido.

| Campo | Regla |
|---|---|
| id | 1–64 letras ASCII, números, guion o guion bajo; unicidad sin distinguir mayúsculas |
| fecha_notificacion | AAAA-MM-DD, fecha real del calendario gregoriano; no se rechazan fechas futuras por no existir ese requisito |
| establecimiento | texto obligatorio, 120 caracteres como máximo |
| distrito | texto obligatorio, 120 caracteres como máximo; filtro exacto, no catálogo geográfico oficial |
| grupo_etario | catálogo didáctico en años: 0-4, 5-11, 12-17, 18-29, 30-59, 60+ |
| evento | valor exacto IRAS |

Todos los campos se recortan en los extremos y rechazan caracteres de control. El catálogo etario es un supuesto académico, no una regla sanitaria oficial. No se calcula edad porque no se recopila fecha de nacimiento.

Una fila con varias infracciones genera un rechazo y una lista de motivos. Solo una aparición válida reserva el ID. La fila del rechazo es la línea física final del registro CSV, contando el encabezado; los registros con saltos de línea entre comillas pueden ocupar más de una línea. La exportación incluye los valores normalizados recibidos en JSON; no pretende preservar byte a byte el archivo original.

Las fechas se convierten a año ISO + W + semana (ejemplo: 2021-01-01 pertenece a 2020-W53). El esquema incluye el año para no mezclar semanas de años distintos. Los filtros son intersecciones exactas y se aplican antes de consolidar. La búsqueda de tablas se realiza en el navegador y no altera el alcance del CSV exportado.

Oráculo previo: datos/entrada/oraculo.json. Semanas 2026-W02 a W06 con 3 notificaciones cada una. Ate, Lima y Comas con 5 cada una. Rechazos en líneas 17, 18, 19, 20 y 21.
