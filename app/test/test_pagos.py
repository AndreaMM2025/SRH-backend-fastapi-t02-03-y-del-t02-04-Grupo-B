from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_pago_1():
    pago = {
        "factura_id": 1,
        "fecha": "2026-01-02",
        "monto": 120.0,
        "metodo": "tarjeta"
    }

    response = client.post("/api/pagos/", json=pago)
    assert response.status_code == 200

    data = response.json()
    assert data["monto"] == 120.0
    assert data["metodo"] == "tarjeta"
    assert "id" in data

def test_crear_pago_2():
    pago = {
        "factura_id": 2,
        "fecha": "2026-02-05",
        "monto": 120.0,
        "metodo": "tarjeta"
    }

    response = client.post("/api/pagos/", json=pago)
    assert response.status_code == 200

    data = response.json()
    assert data["monto"] == 120.0
    assert data["metodo"] == "tarjeta"
    assert "id" in data


def test_listar_pagos():
    response = client.get("/api/pagos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
