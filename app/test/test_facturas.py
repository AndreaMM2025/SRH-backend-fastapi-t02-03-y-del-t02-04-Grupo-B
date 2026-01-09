from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_factura_1():
    factura = {
        "reserva_id": 1,
        "subtotal": 100.0,
        "impuestos": 20.0,
        "total": 120.0
    }

    response = client.post("/api/facturas/", json=factura)
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 120.0
    assert "id" in data

def test_listar_facturas():
    response = client.get("/api/facturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
