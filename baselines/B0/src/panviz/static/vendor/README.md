# Dependencias del navegador

Ejecutar manualmente: `python scripts/preparar_assets.py`.

Descarga Chart.js 4.4.8 y Tailwind CSS 2.2.19 precompilado, con sus licencias MIT. Las versiones están fijadas. No requiere Node/npm ni compilación. Los archivos se sirven desde Flask para funcionar sin conexión después de la preparación.

El diseño principal está en ../css/styles.css y complementa las utilidades Tailwind de las plantillas. Si Chart.js no está disponible, se muestran los datos tabulados. No se incluyen librerías simuladas.
