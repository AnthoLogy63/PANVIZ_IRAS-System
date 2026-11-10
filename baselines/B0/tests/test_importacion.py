"""R01: contract, preview, persistence and exactly-once confirmation."""
import io
from panviz.db import get_db
from panviz.services.csv_service import analyze_csv, CsvError
import pytest

def test_importacion_valida(app, upload, valid_csv):
    response = upload(valid_csv)
    assert response.status_code == 200
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM notifications").fetchone()[0] == 3
        assert get_db().execute("SELECT accepted,rejected FROM batches").fetchone()[:] == (3, 0)

def test_vista_previa_no_guarda(app, upload, valid_csv):
    response = upload(valid_csv, confirm=False)
    assert b"VISTA PREVIA" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM notifications").fetchone()[0] == 0

def test_oraculo_20_filas(app, upload, sample):
    upload(sample)
    with app.app_context():
        db = get_db()
        assert db.execute("SELECT accepted,rejected FROM batches").fetchone()[:] == (15, 5)
        assert [r[0] for r in db.execute("SELECT row_number FROM rejections ORDER BY row_number")] == [17, 18, 19, 20, 21]

def test_reimportacion_no_duplica(app, upload, sample):
    upload(sample)
    upload(sample)
    with app.app_context():
        db = get_db()
        assert db.execute("SELECT COUNT(*) FROM notifications").fetchone()[0] == 15
        assert db.execute("SELECT accepted,rejected FROM batches ORDER BY id DESC LIMIT 1").fetchone()[:] == (0, 20)

def test_confirmacion_un_solo_uso(client, upload, valid_csv):
    upload(valid_csv, confirm=False)
    with client.session_transaction() as session:
        data = {"csrf_token": session["csrf_token"], "token": session["preview_token"]}
    assert client.post("/importacion/confirmar", data=data).status_code == 302
    assert client.post("/importacion/confirmar", data=data).status_code == 400

def test_confirmacion_revalida_duplicados(app, client, upload, valid_csv):
    from panviz.services.csv_service import process_import
    upload(valid_csv, confirm=False)
    with app.app_context():
        db = get_db()
        with db:
            process_import(db, valid_csv, "otro_lote.csv")
    with client.session_transaction() as session:
        data = {"csrf_token": session["csrf_token"], "token": session["preview_token"]}
    assert client.post("/importacion/confirmar", data=data).status_code == 302
    with app.app_context():
        assert get_db().execute("SELECT accepted,rejected FROM batches ORDER BY id DESC LIMIT 1").fetchone()[:] == (0, 3)

@pytest.mark.parametrize("payload", [b"", b"id,evento\nA,IRAS", b"id,id,evento\nA,A,IRAS", b"\xff\xfe"])
def test_contrato_invalido(payload):
    with pytest.raises(CsvError):
        analyze_csv(payload)

def test_delimitador_y_bom(valid_csv):
    result = analyze_csv(b"\xef\xbb\xbf" + valid_csv.replace(b",", b";"))
    assert len(result["accepted"]) == 3

def test_limite_registros(valid_csv):
    with pytest.raises(CsvError, match="Máximo"):
        analyze_csv(valid_csv, max_rows=2)

def test_formulario_protegido(client, valid_csv):
    assert client.post("/importacion/", data={"archivo": (io.BytesIO(valid_csv), "data.csv")}).status_code == 400

def test_seed_una_sola_vez(tmp_path):
    from panviz import create_app
    config = {"DATABASE": str(tmp_path / "seed.sqlite3"), "SEED_DEMO": True, "SECRET_KEY": "test", "TESTING": True}
    first = create_app(config)
    create_app(config)
    with first.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM batches").fetchone()[0] == 1
        assert get_db().execute("SELECT COUNT(*) FROM notifications").fetchone()[0] == 15
