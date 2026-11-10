# Registro de baselines y liberación

| Control | Versión | Quién aprueba | Fecha real | Pendientes / decisión |
|---|---|---|---|---|
| B0 alcance y plan | referencia B0 | E1/E2 pendiente | pendiente | snapshot preparada, revisión humana pendiente |
| B1 código/datos/diseño/pruebas | candidata 0.1.0 | E4 pendiente | pendiente | instalación, ejecución y revisión pendientes |
| B2 liberación | etiqueta v0.1 pendiente | E1/E2/E5 pendientes | pendiente | acta de validación y copia limpia pendientes |

Commit y etiqueta reales: pendiente. Versiones instaladas: se registran en verificacion.json tras ejecutar. Persona distinta que reproduce: pendiente. Resultado desde copia limpia: pendiente. Ruta del ZIP: output/Equipo_Panviz_IRAS_CMMI.zip (a generar). No declarar liberado hasta cerrar los controles.

Reproducción: extraer el ZIP en otra carpeta, crear .venv, instalar requirements, ejecutar scripts/preparar_assets.py si faltan dependencias frontend, ejecutar scripts/verificar.py y python run.py. Confirmar oráculo inicial y CR01 sin copiar instance/.
