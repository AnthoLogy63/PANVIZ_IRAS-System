"""R03: known grouping oracle and ISO year boundaries."""
from panviz.db import get_db
from panviz.services.csv_service import analyze_csv
from panviz.services.consolidation_service import consolidate

def test_consolidacion_conocida(app, upload, valid_csv):
    upload(valid_csv)
    with app.app_context():
        groups = consolidate(get_db())
    assert [(r["semana_iso"],r["distrito"],r["total"]) for r in groups] == [("2026-W02","Lima",2),("2026-W03","Ate",1)]

def test_anio_iso_distinto_del_calendario():
    payload = b"id,fecha_notificacion,establecimiento,distrito,grupo_etario,evento\nY01,2021-01-01,CS Centro,Lima,0-4,IRAS\n"
    assert analyze_csv(payload)["accepted"][0]["semana_iso"] == "2020-W53"

def test_consolidado_oraculo(app, upload, sample):
    upload(sample)
    with app.app_context():
        groups = consolidate(get_db())
    assert len(groups) == 15
    assert sum(r["total"] for r in groups) == 15
    assert {r["semana_iso"] for r in groups} == {"2026-W02","2026-W03","2026-W04","2026-W05","2026-W06"}
