"""R02: independent validation rules, including case insensitive uniqueness."""
import pytest
from panviz.services.csv_service import analyze_csv
from panviz.services.validation_service import validate_record

def record(**changes):
    return {"id":"ABC", "fecha_notificacion":"2026-01-05", "establecimiento":"CS Centro", "distrito":"Lima", "grupo_etario":"0-4", "evento":"IRAS", **changes}

def test_campo_obligatorio_vacio():
    assert any("obligatorio" in error for error in validate_record(record(distrito=""), set()))

def test_fecha_imposible():
    assert any("Fecha imposible" in error for error in validate_record(record(fecha_notificacion="2026-02-30"), set()))

def test_id_duplicado():
    assert any("duplicado" in error for error in validate_record(record(), {"abc"}))

@pytest.mark.parametrize("changes,keyword", [({"evento":"OTRO"},"Evento"),({"grupo_etario":"121+"},"Grupo"),({"id":"=A1"},"Formato"),({"fecha_notificacion":"05/01/2026"},"Fecha"),({"distrito":"x"*121},"Longitud"),({"establecimiento":"CS\tCentro"},"control")])
def test_formatos_invalidos(changes, keyword):
    assert any(keyword in error for error in validate_record(record(**changes), set()))

def test_anio_bisiesto():
    assert not validate_record(record(fecha_notificacion="2024-02-29"), set())

def test_fila_columnas_incorrectas(valid_csv):
    result = analyze_csv(valid_csv + b"A004,2026-01-05,CS Centro,Lima,0-4,IRAS,extra\n")
    assert len(result["accepted"]) == 3
    assert "columnas" in result["rejected"][0]["motivo"]

def test_id_invalido_no_reserva_clave(valid_csv):
    text = valid_csv.decode().splitlines()
    payload = (text[0] + "\nA001,2026-02-30,CS Centro,Lima,0-4,IRAS\n" + text[1] + "\n").encode()
    result = analyze_csv(payload)
    assert len(result["accepted"]) == 1
    assert len(result["rejected"]) == 1
