"""R04: actual endpoint exports reconcile and protect spreadsheet consumers."""
import csv
import io
import pytest
from panviz.services.export_service import reconcile, safe_cell

def csv_rows(response):
    return list(csv.DictReader(io.StringIO(response.data.decode("utf-8-sig"))))

def test_reconciliacion_y_exportacion(client, upload, valid_csv):
    upload(valid_csv)
    response = client.get("/reportes/consolidado.csv")
    assert response.status_code == 200
    assert "attachment" in response.headers["Content-Disposition"]
    rows = csv_rows(response)
    assert len(rows) == 2
    assert sum(int(row["total"]) for row in rows) == 3

def test_exporta_rechazos(client, upload, sample):
    upload(sample)
    rows = csv_rows(client.get("/reportes/rechazos.csv?lote=1"))
    assert len(rows) == 5
    assert [int(row["fila"]) for row in rows] == [17,18,19,20,21]
    assert all(row["motivo"] and row["datos_originales"] for row in rows)

def test_reconciliacion_detecta_diferencia():
    with pytest.raises(ValueError):
        reconcile([{"total":2}],3)

def test_proteccion_formulas():
    for value in ("=SUM(A1)", "+1", "-1", "@SUM(A1)", "  =A1"):
        assert safe_cell(value).startswith("'")

def test_exportacion_vacia_conserva_contrato(client):
    response = client.get("/reportes/consolidado.csv")
    assert response.status_code == 200
    assert csv_rows(response) == []
    assert "semana_iso" in response.data.decode("utf-8-sig")
