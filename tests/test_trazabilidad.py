"""R05: requirement links must resolve to actual source and test artifacts."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_r05_enlaces_trazabilidad():
    with (ROOT / "docs/requisitos/trazabilidad.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["id"] for row in rows} == {"R01", "R02", "R03", "R04", "R05", "CR01"}
    for row in rows:
        assert (ROOT / row["diseno"]).is_file()
        assert (ROOT / row["codigo"]).is_file()
        assert (ROOT / row["prueba"].split("::")[0]).is_file()
        assert row["version"] and row["evidencia"]
