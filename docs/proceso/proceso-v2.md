# Proceso estándar v2 · revisión propuesta por inspección estática

Mantiene los siete pasos y roles de v1. Cambio: antes de solicitar revisión humana o liberar, aplicar un punto de control de coherencia estática y ejecución real.

- Revisar delimitadores y referencias de módulos, rutas y plantillas.
- Incluir lotes inexistentes, reimportación, confirmación repetida, vista previa desactualizada y cambio de año ISO en la verificación.
- Guardar salida real de pytest, versiones y comparación con el oráculo mediante scripts/verificar.py.
- Separar explícitamente implementación, inspección estática, ejecución automatizada y aprobación por el equipo. Una no sustituye a las otras.
- Usar en la pantalla y exportación la misma función de filtros y reconciliar después de filtrar.

Justificación NC01: la inspección de la fuente detectó dos expresiones con paréntesis sobrante en tests/test_filtro_distrito.py; se corrigieron antes de solicitar ejecución. También se detectó que un lote inexistente mostraba tarjetas del historial global: ahora retorna 404. La mejora del proceso es verificar sintaxis y alcance de consultas antes de B1. Estas observaciones corresponden a inspección estática; la revisión por pares y los resultados de pytest se registran por separado.

Evaluación de eficacia: pendiente de la primera ejecución y la revisión E4. Aprobación de v2 por E1: pendiente. Solo tras estas actividades se puede afirmar que la mejora fue validada en el piloto.
