"""Build the academic ZIP only after manual verification and Git tagging."""
import json
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from source_fingerprint import source_fingerprint

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".venv", "__pycache__", ".pytest_cache", "instance", "output", "node_modules"}

def main():
    evidence = ROOT / "evidencias/verificacion.json"
    if not evidence.exists() or json.loads(evidence.read_text(encoding="utf-8")).get("pytest_exit_code") != 0:
        raise SystemExit("Primero ejecuta scripts/verificar.py y corrige todos los fallos.")
    if json.loads(evidence.read_text(encoding="utf-8")).get("source_sha256") != source_fingerprint(ROOT):
        raise SystemExit("El código cambió después de la verificación. Ejecuta scripts/verificar.py de nuevo.")
    if not (ROOT / ".git").exists():
        raise SystemExit("Falta el historial Git requerido por el trabajo. Consulta README.md.")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        tag = subprocess.check_output(["git", "rev-parse", "v0.1^{commit}"], cwd=ROOT, text=True).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        raise SystemExit("Git o etiqueta v0.1 no disponibles. Consulta README.md.") from error
    if head != tag or dirty:
        raise SystemExit("v0.1 debe apuntar a HEAD y no debe haber cambios en archivos versionados.")
    for asset in ("chart.umd.js", "tailwind.min.css"):
        if not (ROOT / "src/panviz/static/vendor" / asset).exists():
            raise SystemExit("Faltan assets locales: ejecuta scripts/preparar_assets.py antes de crear la entrega.")
    output = ROOT / "output/Equipo_Panviz_IRAS_CMMI.zip"
    output.parent.mkdir(exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for item in sorted(ROOT.rglob("*")):
            relative = item.relative_to(ROOT)
            if any(part in EXCLUDED for part in relative.parts) or not item.is_file() or item.is_symlink():
                continue
            archive.write(item, Path("Equipo_Panviz_IRAS_CMMI") / relative)
    print(f"Paquete creado: {output}")
    print("Revisa que actas, informe y contribuciones del equipo estén completos antes de entregarlo.")

if __name__ == "__main__":
    main()
