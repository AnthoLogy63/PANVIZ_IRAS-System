"""Integration smoke checks against the real Jinja templates."""
import pytest

@pytest.mark.parametrize("url", ["/", "/importacion/", "/validacion/", "/reportes/"])
def test_pagina_vacia(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert "PANVIZ" in response.text
    assert '<html lang="es">' in response.text

@pytest.mark.parametrize("url", ["/", "/importacion/", "/validacion/", "/reportes/"])
def test_pagina_con_datos(client, upload, sample, url):
    upload(sample)
    assert client.get(url).status_code == 200

def test_no_encontrado(client):
    assert client.get("/no-existe").status_code == 404

def test_csrf_no_se_expone_en_export(client):
    response = client.get("/reportes/consolidado.csv")
    assert "csrf_token" not in response.text


def test_lote_inexistente_devuelve_404(client):
    assert client.get("/validacion/?lote=999").status_code == 404
