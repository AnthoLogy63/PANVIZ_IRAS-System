"""CR01: district scope must agree across UI, consolidation and export."""
import csv
import io
from panviz.db import get_db
from panviz.services.consolidation_service import consolidate

def test_cr01_filtro_distrito(app, client, upload, sample):
    upload(sample)
    with app.app_context():
        groups = consolidate(get_db(), {"distrito":"Ate"})
    assert sum(r["total"] for r in groups) == 5
    assert all(r["distrito"] == "Ate" for r in groups)
    response = client.get("/reportes/consolidado.csv?distrito=Ate")
    rows = list(csv.DictReader(io.StringIO(response.data.decode("utf-8-sig"))))
    assert sum(int(r["total"]) for r in rows) == 5
    assert {r["distrito"] for r in rows} == {"Ate"}
    assert "5 consolidados = 5 aceptados" in client.get("/reportes/?distrito=Ate").text
    assert '"Ate": 5' in client.get("/?distrito=Ate").text

def test_distrito_inexistente(client, upload, sample):
    upload(sample)
    response = client.get("/reportes/consolidado.csv?distrito=Inexistente")
    assert len(list(csv.DictReader(io.StringIO(response.data.decode("utf-8-sig"))))) == 0

def test_filtro_no_modifica_datos(app, client, upload, sample):
    upload(sample)
    client.get("/reportes/?distrito=Lima")
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM notifications").fetchone()[0] == 15

def test_baseline_sin_cr01(app, client, upload, sample):
    upload(sample)
    app.config["DISTRICT_FILTER_ENABLED"] = False
    response = client.get("/reportes/consolidado.csv?distrito=Ate")
    rows = list(csv.DictReader(io.StringIO(response.data.decode("utf-8-sig"))))
    assert sum(int(r["total"]) for r in rows) == 15
    assert "CR01 · filtro" not in client.get("/reportes/").text

def test_filtros_combinados(client, upload, sample):
    upload(sample)
    response = client.get("/reportes/consolidado.csv?distrito=Ate&semana_iso=2026-W02&grupo_etario=18-29")
    rows = list(csv.DictReader(io.StringIO(response.data.decode("utf-8-sig"))))
    assert len(rows) == 1
    assert rows[0]["total"] == "1"
