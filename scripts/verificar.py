"""Manual verification entry point: real pytest output and oracle measurements."""
import importlib.metadata
import json
import platform
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from source_fingerprint import source_fingerprint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def main():
    evidence = ROOT / "evidencias"
    evidence.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    junit = evidence / f"pytest-{stamp}.xml"
    command = [sys.executable, "-m", "pytest", "-q", f"--junitxml={junit}"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    output = result.stdout + result.stderr
    print(output)
    (evidence / f"pytest-{stamp}.txt").write_text(output, encoding="utf-8")
    data = {"fecha_utc": stamp, "python": platform.python_version(), "plataforma": platform.platform(), "pytest_exit_code": result.returncode, "junit": junit.name, "comando": command, "aprobaciones_humanas": "pendientes", "source_sha256": source_fingerprint(ROOT)}
    for package in ("Flask", "pytest"):
        try:
            data[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            data[package] = "no instalado"
    if result.returncode == 0:
        from panviz import create_app
        from panviz.db import get_db
        from panviz.services.csv_service import process_import
        from panviz.services.consolidation_service import consolidate
        from panviz.services.export_service import reconcile
        oracle = json.loads((ROOT / "datos/entrada/oraculo.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as folder:
            app = create_app({"DATABASE": str(Path(folder) / "oracle.sqlite3"), "SEED_DEMO": False, "SECRET_KEY": "verification-only", "TESTING": True})
            with app.app_context():
                db = get_db()
                with db:
                    batch = process_import(db, (ROOT / "datos/entrada/notificaciones_iras.csv").read_bytes(), "notificaciones_iras.csv")
                total = reconcile(consolidate(db), len(batch["accepted"]))
                data["oraculo"] = {"aceptados": len(batch["accepted"]), "rechazados": len(batch["rejected"]), "consolidados": total, "diferencia": total-len(batch["accepted"]), "deteccion_errores_porcentaje": len(batch["rejected"])/oracle["rechazados"]*100, "por_distrito": {district: sum(r["total"] for r in consolidate(db, {"distrito": district})) for district in oracle["por_distrito"]}}
                if (len(batch["accepted"]), len(batch["rejected"]), total) != (15, 5, 15) or data["oraculo"]["por_distrito"] != oracle["por_distrito"]:
                    data["pytest_exit_code"] = 1
                    data["error"] = "El oráculo no coincide"
    (evidence / f"verificacion-{stamp}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (evidence / "verificacion.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Evidencia guardada en evidencias/. Aprobaciones humanas siguen pendientes.")
    return data["pytest_exit_code"]

if __name__ == "__main__":
    raise SystemExit(main())
