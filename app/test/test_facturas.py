from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_factura_1():
    factura = {
        "ID_FACTURA": 1,
        "ID_RESERVA": 1,
        "SUBTOTAL": 100.0,
        "IMPUESTOS": 20.0,
        "TOTAL": 120.0
    }

    response = client.post("/api/facturas/", json=factura)
    assert response.status_code == 200

    data = response.json()
    assert data["ID_FACTURA"] == 1
    assert data["TOTAL"] == 120.0


def test_listar_facturas():
    response = client.get("/api/facturas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
