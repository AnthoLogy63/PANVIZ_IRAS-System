# PANVIZ IRAS

Aplicación web local de vigilancia académica de infecciones respiratorias agudas. Flask + Jinja2 + SQLite + Tailwind CSS + JavaScript + Chart.js. Datos exclusivamente sintéticos. Versión candidata 0.1.0.

## Preparación en Windows / PowerShell

Desde la carpeta que contiene este README, ejecutar manualmente este bloque. Python 3.10 o superior debe estar instalado. SQLite viene incluido con Python; no se instala un servidor. No se necesita Node ni npm. La descarga inicial de dependencias requiere internet.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/preparar_assets.py
.\.venv\Scripts\python.exe scripts/verificar.py
.\.venv\Scripts\python.exe run.py
```

Abrir http://127.0.0.1:5000. Detener con Ctrl+C. Usar el ejecutable de .venv evita problemas de ExecutionPolicy. Si el comando py no existe, sustituir solamente el primer comando por `python -m venv .venv`. Si falla un paso, detenerse y revisar su salida antes de continuar.

## Demostración

La primera ejecución crea instance/panviz.sqlite3 y carga una vez el ejemplo: 15 notificaciones aceptadas, 5 rechazadas, 3 distritos y 5 semanas. El dashboard utiliza exclusivamente SQLite. La carga automática aparece como lote de demostración. No se vuelve a cargar al reiniciar.

1. Dashboard: revisar tendencias, cobertura y notificaciones recientes.
2. Validación: consultar el lote inicial; exportar 5 rechazos con fila y motivo.
3. Reportes: confirmar 15 consolidados = 15 aceptados; filtrar Ate para obtener 5; exportar CSV y comparar.
4. Importación: descargar el ejemplo, cargarlo, analizar y confirmar. Como la demo ya existe, los 15 registros previamente aceptados se rechazan por duplicidad: segundo lote con 0 aceptados y 20 rechazos. Este resultado es correcto. Para aceptar nuevos registros, usar ID nuevos o importar solo correcciones de rechazos.

El oráculo inicial de 15/5 corresponde a una base vacía. `scripts/verificar.py` usa bases temporales independientes y no modifica la base de demostración.

## Funcionalidad

- Cuatro pantallas adaptables, menú plegable, búsqueda visual y ordenamiento de tablas.
- CSV UTF-8, BOM opcional, coma o punto y coma, máximo 2 MB y 10 000 filas.
- Vista previa con confirmación; revalidación bajo transacción SQLite.
- Validación de campos, fecha ISO, catálogo etario, evento IRAS, duplicados en el archivo y entre lotes.
- Agrupación por año/semana ISO, establecimiento, distrito y grupo etario.
- Exportación consolidada y de rechazos; misma selección de filtros; protección frente a fórmulas de hojas de cálculo.
- Persistencia de lotes, notificaciones, rechazos y vistas previas temporales. Formularios protegidos con token CSRF.

## Organización

```text
src/panviz/          factory, configuración y SQLite
  routes/           dashboard, importación, validación, reportes
  services/         CSV, reglas, consolidación, exportación
  templates/        páginas Jinja y componentes
  static/           estilos, scripts, marca y dependencias locales
datos/entrada/      20 filas y oráculo previo
datos/salida/       destino opcional para CSV descargados
tests/              pruebas unitarias y de integración
docs/requisitos/    R01-R05, CR01, catálogo y trazabilidad
docs/proceso/       v1, v2, adaptación, plantillas y formación
docs/gestion/       diseño, decisiones, riesgos, seguimiento, baselines
evidencias/         índice, revisión, validación y resultados reales
baselines/B0/       instantánea funcional sin habilitar CR01
scripts/            preparación, verificación y empaquetado
```

## Pruebas y evidencia

`python scripts/verificar.py` ejecuta pytest, guarda salida con fecha UTC y JUnit, registra versiones reales y calcula el resultado del conjunto inicial en una SQLite temporal. No inventa resultados. Las actas humanas siguen pendientes hasta que el equipo las complete. También se puede ejecutar `python -m pytest -q`.

Para reproducir el comportamiento previo al filtro: `python run.py --baseline`. En ese perfil el parámetro distrito no se aplica a las consultas HTTP. La instantánea independiente está en baselines/B0; consultar docs/gestion/baselines.md. El perfil es una referencia funcional reproducible, no un historial Git inventado.

## Git y paquete académico

Git es un requisito del trabajo. Una vez que las pruebas y la revisión del equipo hayan terminado, ejecutar manualmente:

```powershell
git init
git add .
git commit -m "Implementa PANVIZ IRAS con SQLite y CR01"
git tag -a v0.1 -m "Entrega académica PANVIZ IRAS"
.\.venv\Scripts\python.exe scripts/empaquetar.py
```

Configurar nombre/correo de Git si Git lo solicita; usar los datos reales del integrante. No se crean contribuciones ni aprobaciones ficticias. El ZIP se genera en output/Equipo_Panviz_IRAS_CMMI.zip e incluye .git cuando existe. El script exige pruebas satisfactorias y la etiqueta v0.1 apuntando al commit actual, sin cambios pendientes en archivos versionados. Deben conservarse y registrarse las revisiones cruzadas reales; un único commit no demuestra contribución individual de cinco integrantes.

## Documentación y pendientes de entrega

Leer docs/INFORME.md o abrir docs/informe.html e imprimir a PDF (A4, escala 100 %, encabezados del navegador desactivados): siete páginas previstas, pendientes de revisar en el equipo local. Incluye pendientes explícitos de ejecución y del artículo de apoyo, que no se adjuntó a esta carpeta. docs/DEMOSTRACION.md contiene un guion de ocho minutos.

El sistema está orientado a demostración local. No incorpora diagnóstico, autenticación ni usuarios. SQLite y la clave local se conservan en instance/; respaldar esa carpeta con la aplicación detenida. No compartir la base ni la clave. El servidor escucha solo en 127.0.0.1. La revisión visual en navegador y la ejecución de Python quedan pendientes de los comandos manuales del usuario. No se afirma certificación ni madurez CMMI formal.
