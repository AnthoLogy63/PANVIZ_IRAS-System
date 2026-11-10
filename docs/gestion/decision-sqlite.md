# DAR-01 · Persistencia local

Fecha de diseño: 2026-11-10. Decisión autorizada por el usuario: usar SQLite. Responsable académico propuesto: E3; revisión del equipo pendiente.

Escala 1–5 (mejor). Pesos: simplicidad 35 %, integridad 30 %, reproducibilidad 25 %, concurrencia 10 %.

| Alternativa | Simplicidad | Integridad | Reproducibilidad | Concurrencia | Total |
|---|---:|---:|---:|---:|---:|
| CSV/JSON como almacenamiento | 5 | 2 | 4 | 1 | 3.45 |
| SQLite + sqlite3 | 5 | 5 | 5 | 3 | 4.80 |
| PostgreSQL | 2 | 5 | 2 | 5 | 3.20 |

Se elige SQLite: viene con Python, mantiene integridad y transacciones, evita servicio adicional. Su concurrencia de escritura es limitada y suficiente para la demostración local. Las alternativas y puntuaciones son valoración de diseño, no mediciones de rendimiento.

Otras decisiones: seis campos del contrato original; grupo etario explícito; fechas reales sin límite de futuro; duplicados sin distinguir mayúsculas; confirmar bajo bloqueo para evitar que una vista previa desactualizada omita duplicados. Fuente de alcance: instrucción del usuario y especificación docente.
