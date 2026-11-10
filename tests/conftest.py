import io
from pathlib import Path
import pytest
from panviz import create_app

@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "SECRET_KEY": "test-only", "DATABASE": str(tmp_path / "test.sqlite3"), "SEED_DEMO": False})

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample():
    return (Path(__file__).resolve().parents[1] / "datos/entrada/notificaciones_iras.csv").read_bytes()

@pytest.fixture
def valid_csv():
    return b"id,fecha_notificacion,establecimiento,distrito,grupo_etario,evento\nA001,2026-01-05,CS Centro,Lima,0-4,IRAS\nA002,2026-01-06,CS Centro,Lima,0-4,IRAS\nA003,2026-01-12,CS Este,Ate,18-29,IRAS\n"

@pytest.fixture
def upload(client):
    def perform(payload, filename="entrada.csv", confirm=True):
        client.get("/importacion/")
        with client.session_transaction() as session:
            csrf = session["csrf_token"]
        response = client.post("/importacion/", data={"csrf_token": csrf, "archivo": (io.BytesIO(payload), filename)}, content_type="multipart/form-data")
        if response.status_code != 200 or not confirm:
            return response
        with client.session_transaction() as session:
            token = session["preview_token"]
        return client.post("/importacion/confirmar", data={"csrf_token": csrf, "token": token}, follow_redirects=True)
    return perform
