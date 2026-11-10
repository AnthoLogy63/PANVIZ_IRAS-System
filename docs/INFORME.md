# PANVIZ IRAS · Informe académico

Versión candidata 0.1.0 · 2026-11-10 · Equipo: pendiente de identificar

## 1. Objetivo y alcance

PANVIZ IRAS es un piloto académico para mejorar la calidad y trazabilidad de un flujo de notificaciones de infecciones respiratorias agudas. El producto desarrollado es una aplicación local con cuatro pantallas: dashboard, importación, validación y reportes consolidados. Su alcance incluye recepción CSV, validación de datos, consolidación semanal, exportación y gestión documental del cambio CR01.

La fuente de requisitos es la especificación docente trab_81.pdf. No se dispone de información sobre un sistema sanitario real: los datos y problemas tratados son supuestos didácticos. No se implementan diagnóstico clínico, autenticación ni gestión de personas. La información de entrada es exclusivamente sintética y contiene seis campos: id, fecha_notificacion, establecimiento, distrito, grupo_etario y evento. El evento permitido es IRAS y el catálogo etario es una decisión documentada del piloto.

El usuario autorizó usar SQLite. Esta decisión permite conservar lotes, aceptaciones y rechazos sin instalar un servidor adicional. Se mantiene una sola aplicación Flask con factory, Blueprints, Jinja2, JavaScript, Tailwind y Chart.js. La base y la clave local se crean durante la primera ejecución.

Se prepararon fuentes, pruebas, documentación y registros. El conjunto inicial y su oráculo se definieron antes de ejecutar: 20 filas, 15 aceptadas y 5 rechazadas. Los resultados de pruebas y las aprobaciones se respaldan con sus registros de ejecución y actas. Este informe mantiene pendientes los resultados que aún no cuentan con evidencia adjunta.

Evidencia EV01: requisitos, catálogo, oráculo y matriz de trazabilidad. Los criterios de cierre deben revisarse con los integrantes reales antes de declarar aprobadas las baselines.

---

## 2. Lecciones del artículo de apoyo

La consigna identifica el trabajo de Liberato, Varajão y Martins (2015), “CMMI Implementation and Results: The Case of a Software Company”, DOI 10.4018/978-1-4666-7473-8.ch003, y orienta la lectura de las páginas 54–57 y 58–60. En la carpeta se recibió la consigna de seis páginas, pero no el artículo de apoyo. Esta sección registra lecciones indicadas por la consigna; la verificación directa de páginas y contexto del artículo queda pendiente. No se presentan citas textuales ni se atribuye una lectura que no se realizó.

Primera lección asignada: definir procesos con los usuarios. La decisión aplicada es documentar R01–R05 y CR01 con criterios observables y reservar a E2 la validación del escenario completo. El usuario simulado debe contrastar esperado, observado y decisión; el desarrollo no equivale a aceptación. Referencia de lectura sugerida en la consigna: páginas 54–57; página precisa por confirmar.

Segunda lección asignada: probar antes de extender. El piloto utiliza un conjunto pequeño con oráculo previo, SQLite temporal en pruebas y una referencia funcional sin CR01. La regresión debe ejecutarse antes de liberar. Solo después de reunir evidencia puede proponerse otro módulo. Referencia sugerida: páginas 54–57; detalle pendiente de contraste.

Tercera lección asignada: reducir carga documental mediante plantillas y soporte común. Se utilizan Markdown y CSV para requisitos, pruebas, cambios y revisión. La decisión evita introducir un gestor documental externo. Las plantillas conservan campos de autor, revisor, versión y resultado. Referencia sugerida: páginas 54–57; resultado del estudio a contrastar en 58–60.

La consigna describe opiniones de 22 jefes de proyecto y un periodo inicial del caso. No corresponde transferir sus resultados al piloto ni afirmar que este desarrollo alcanza madurez organizacional. El equipo debe completar el contraste del artículo antes de entregar la versión final.

---

## 3. Diagnóstico y correspondencia CMMI

El diagnóstico se limita a la evidencia inicial de esta carpeta: una propuesta de estructura y la consigna docente. No existían fuentes de aplicación, pruebas, proceso común ni registros de revisión. Esta ausencia permite definir tres brechas del trabajo académico sin atribuir problemas reales a Panviz.

Brecha de trazabilidad: no había enlaces entre requisitos, implementación y pruebas. Acción: crear una matriz que vincule R01–R05 y CR01 con diseño, código, pruebas, versión y evidencias. La estructura ya está preparada; la revisión nominativa y el historial de configuración siguen pendientes.

Brecha de proceso común: no había un procedimiento reutilizable con adaptación. Acción: publicar proceso v1, plantillas y regla CSV/formulario; conservar v1 y proponer v2 a partir de una incidencia estática real. La adopción y aprobación del estándar deben comprobarse con el equipo.

Brecha de revisión: no existían resultados de ejecución ni dictamen independiente. Acción: suite pytest, script de evidencia, lista de calidad y acta de validación. Ninguno de estos archivos demuestra por sí mismo que la revisión o la aceptación ocurrieron.

El marco histórico empleado es CMMI DEV v1.3. La matriz cubre las siete áreas de nivel 2: REQM, PP, PMC, SAM, MA, PPQA y CM; y las once de nivel 3: RD, TS, PI, VER, VAL, OPF, OPD, OT, IPM, RSKM y DAR. Se utilizan los estados no evidenciada, parcial, demostrada en el piloto y no aplicable con justificación.

SAM se considera no aplicable al alcance actual porque no existe adquisición contratada; instalar bibliotecas no basta para evidenciar gestión de proveedores. Las restantes áreas están parciales o no evidenciadas según la actividad pendiente. La matriz no declara cumplimiento completo por disponer de documentos. Evidencias EV01, EV03 y EV07.

---

## 4. Proceso estándar y adaptación

El proceso sigue un ciclo breve: diagnosticar, planificar, definir, ejecutar, evaluar y ajustar. La versión v1 establece requisitos verificables, diseño, oráculo previo, implementación, revisión por una persona distinta, pruebas, cambio controlado y liberación reproducible. Los puntos B0, B1 y B2 requieren identificar aprobador, fecha, versión y pendientes.

La adaptación aplicada al piloto sustituye mecanismos externos por archivos Markdown/CSV y herramientas locales. La recepción CSV exige una prueba de contrato de seis columnas, UTF-8 y límites de tamaño. En otro módulo con formulario, la prueba de encabezados se sustituiría por contrato de campos; se conservarían trazabilidad, oráculo, revisión y cambio controlado. No se construye ese segundo módulo.

CR01 pide filtrar el consolidado por distrito. El criterio previo es concreto: Ate produce cinco aceptadas y total exportado cinco; distrito inexistente produce cero; limpiar filtros restaura quince. Se documentaron impacto, regresión y responsables. La autorización del usuario permite implementar la funcionalidad; no se inventa una aprobación académica de E1. Esta se mantiene pendiente en el registro.

La referencia funcional B0 conserva el comportamiento sin distrito. El perfil --baseline permite compararlo y la instantánea independiente contiene su propio origen, configuración y datos. No se presenta como un historial Git previo que no existe.

NC01 surgió durante inspección estática: dos expresiones de las pruebas contenían un cierre de paréntesis sobrante y la consulta de un lote inexistente podía mostrar totales globales. Se corrigieron ambos casos. La propuesta v2 añade revisión de coherencia y alcance de estados de error antes de B1. La evaluación de eficacia, ejecución real y verificación de cierre por E4 siguen pendientes. EV07 conserva esta distinción.

---

## 5. Herramientas y responsabilidades

Flask organiza las rutas y sirve Jinja2 y los recursos estáticos desde un solo proceso. Los servicios separan contrato CSV, validación, consolidación y exportación. SQLite utiliza claves únicas, claves foráneas y transacciones. La confirmación revalida duplicados bajo bloqueo de escritura para evitar que una vista previa desactualizada inserte registros repetidos.

Tailwind precompilado complementa los estilos propios; Chart.js presenta agregados de datos aceptados. Un script manual descarga versiones fijadas para usarlas localmente sin Node ni npm. El diseño principal y las tablas siguen siendo locales; preparar los assets es un paso requerido de instalación.

Pytest cubre reglas y rutas con SQLite temporal. scripts/verificar.py ejecuta la suite, guarda salida y JUnit con fecha UTC, registra versiones reales y contrasta el oráculo sin alterar la demo. Git debe conservar contribuciones reales, revisión y etiqueta v0.1. El empaquetado comprueba evidencia de tests y consistencia de etiqueta antes de producir el ZIP.

Roles propuestos por la consigna: E1 coordina, decide y responde por la entrega; E2 desarrolla requisitos y valida como usuario simulado; E3 diseña y programa; E4 revisa código, prueba y audita calidad; E5 administra configuración y medición. Los nombres reales deben asignarse en los registros. E3 no aprueba su propio código; E1 revisa registros de E4 y evidencia de E5.

La formación de quince minutos incluye localizar una plantilla y explicar su criterio de cierre. Se preparó un registro de cinco integrantes sin completar asistencias ficticias. La ejecución desde copia limpia debe hacerla otra persona. EV03, EV05 y EV06 permanecen pendientes hasta estas actividades.

---

## 6. Resultados previstos y mediciones

Este apartado diferencia lo preparado de lo observado. Se han escrito el backend, las cuatro pantallas, las reglas de datos, el conjunto sintético, la suite, CR01 y la documentación. La ejecución de pruebas, la configuración de versiones y la inspección visual deben respaldarse con evidencia verificable. La inspección estática no prueba el funcionamiento completo.

Oráculo inicial sobre base vacía: veinte filas, quince aceptadas, cinco rechazadas, quince grupos y diferencia de reconciliación cero. Las semanas 2026-W02 a W06 contienen tres registros cada una. Ate, Comas y Lima tienen cinco aceptadas cada uno. Las líneas 17–21 representan duplicado, distrito vacío, fecha imposible, edad fuera del catálogo y evento incorrecto. Una segunda carga idéntica debe producir cero aceptadas y veinte rechazos.

La suite contempla las seis categorías iniciales y CR01, además de contratos, reimportación, protección CSRF, confirmación de un solo uso, revalidación de una vista previa, exportación vacía, fórmulas CSV y límites del año ISO. Es cobertura preparada, no cantidad de pruebas aprobadas. El total observado se tomará del JUnit generado.

Indicadores docentes: trazabilidad completa de seis elementos; cien por ciento de pruebas satisfactorias, al menos siete; detección de cinco inválidas sin falsos rechazos; reconciliación cero antes y después del filtro; cinco comprobaciones de formación y revisión del cien por ciento de productos sometidos. Los porcentajes deben calcularse con denominadores realmente observados.

Para completar EV02 se ejecuta scripts/verificar.py y se conserva toda salida, incluso fallos previos. E5 interpreta los valores y E4 revisa las incidencias. El equipo debe registrar dos cortes de avance y una acción sobre desviación. EV04 recoge esperado, observado y decisión de aceptación. Hasta entonces, los resultados de ejecución y aceptación permanecen pendientes.

---

## 7. Brechas restantes y continuidad

El producto queda preparado para instalación y demostración local, con comprobaciones manuales pendientes. Las acciones inmediatas son instalar el entorno y assets, ejecutar la suite, corregir cualquier fallo observado, revisar la interfaz en escritorio/móvil y completar una prueba de uso integral. Solo estos pasos permiten afirmar funcionamiento verificado en el equipo del usuario.

En calidad y proceso faltan revisión por pares nominativa, validación E2, aprobación E1, formación de cinco integrantes, dos cortes de seguimiento y evaluación de la mejora NC01. En configuración faltan historial Git real, contribuciones identificables, etiqueta v0.1 y reproducción por otra persona desde una copia limpia. El informe requiere contraste directo del artículo de apoyo y sustitución de resultados previstos por valores observados.

La liberación no debe cerrar pendientes por disponer de documentos. El ZIP académico se genera tras conservar la evidencia real y etiquetar el commit revisado. Se excluyen entorno virtual, cachés y almacenamiento local; se conserva el historial Git si existe. La revisión final debe confirmar el contenido y la paginación del informe, prevista en siete páginas sin anexos.

Continuidad H1: repetir el proceso en otro módulo. Responsable propuesto E3 con apoyo de E2; evidencia esperada: adaptación, contrato, oráculo y validación. H2: reunir evidencia sostenida de varios ciclos y extenderla a la unidad académica. Responsable E1/E5; evidencia: series de indicadores, acuerdos y acciones cerradas. H3: revisar todas las brechas y preparar una evaluación conforme al modelo aplicable. Responsable E4; evidencia: matriz con trazabilidad y revisiones independientes.

La demostración dura ocho minutos: tres para el flujo, dos para CR01 y trazabilidad, dos para proceso y mejora y uno para brechas y roles. El piloto demuestra prácticas seleccionadas únicamente cuando estas se ejecutan y documentan. No constituye certificación, efectividad clínica ni declaración formal de madurez tres. La entrega prioriza evidencia reproducible y pendientes honestos.