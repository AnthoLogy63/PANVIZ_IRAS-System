# Adaptación aplicada y reutilización

Proceso estándar: docs/proceso/proceso-v2.md. Aplicación piloto: importación CSV local, conjunto sintético, datos sin identificadores de personas, SQLite, revisión y pruebas reproducibles. Se adapta la recepción al contrato de seis columnas y UTF-8. Se mantiene sin excepciones el oráculo previo, la revisión cruzada, la trazabilidad y el registro de cambios.

Ejemplo reutilizable para otro módulo (no construido): una entrada por formulario de vacunación sustituiría la prueba de encabezados por campos obligatorios/formatos del formulario y conservaría las plantillas de requisito, cambio, prueba y revisión. El responsable debe documentar el catálogo y el alcance antes de programar. Este ejemplo no define reglas clínicas.

Proporcionalidad: no se requiere servidor de BD ni gestor documental externo. Markdown y CSV cubren procesos/medición. El usuario pidió SQLite; la decisión se documenta en DAR-01. La comprobación automatizada no reemplaza las firmas de E1/E2/E4 ni las contribuciones de los integrantes.
