# Baselines y configuración

B0: comportamiento de R01–R04 sin filtro por distrito; requisitos y oráculo definidos. Snapshot independiente en baselines/B0 y manifiesto SHA-256 en baselines/B0/manifest.json. Ejecutar su run.py tras instalar las mismas dependencias. Sus rutas relativas apuntan a sus propios src/, datos/ e instance/.

La snapshot se creó durante esta entrega con distrito deshabilitado; no representa un commit previo firmado. El código compartido incluye soporte configurable de CR01, pero en B0 no expone ni aplica distrito. También puede compararse funcionalmente con python run.py --baseline, usando la base principal.

B1: fuente actual con CR01, revisión y regresión pendientes. B2: aceptación del usuario simulado, revisión E4, etiqueta v0.1 y reproducción desde copia limpia; pendiente. Registrar nombres reales, fecha y pendientes en evidencias/liberacion.md.

Elementos controlados: código, datos sintéticos, oráculo, tests, requirements, documentación, scripts y dependencias frontend descargadas. Elementos locales excluidos: .venv, cachés, instance, archivos temporales y ZIP de salida. Git lo inicia y opera el usuario manualmente. Los resultados de pruebas y actas deben conservarse en el repositorio antes de etiquetar.

No se reconstruye historial ni se atribuyen commits a integrantes inexistentes. La matriz de trazabilidad es enlace estructural; la aprobación y ejecución son evidencias distintas.
