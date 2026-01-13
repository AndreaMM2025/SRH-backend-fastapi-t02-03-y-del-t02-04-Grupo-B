from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_factura_1():
    factura = {
        "cliente_id": 1,
        "reserva_id": 1,
        "total": 120.0,
        "fecha": "2026-01-02"
    }

    response = client.post("/api/facturas/", json=factura)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 1
    assert data["reserva_id"] == 1
    
    assert data["total"] == 120.0
    assert data["fecha"] == "2026-01-02"

def test_crear_factura_2():
    factura = {
        "cliente_id": 2,
        "reserva_id": 2,
        "total": 200.0,
        "fecha": "2026-02-05"
    }

    response = client.post("/api/facturas/", json=factura)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 2
    assert data["reserva_id"] == 2

    assert data["total"] == 200.0
    assert data["fecha"] == "2026-02-05"

def test_listar_facturas():
    response = client.get("/api/facturas/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)

def test_crear_factura_3():
    factura = {
        "cliente_id": 3,
        "reserva_id": 3,
        "total": 300.0,
        "fecha": "2026-03-05"
    }

    response = client.post("/api/facturas/", json=factura)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 3
    assert data["reserva_id"] == 3

    assert data["total"] == 300.0
    assert data["fecha"] == "2026-03-05"


def test_crear_factura_4():
    factura = {
        "cliente_id": 4, 
        "reserva_id": 4, 
        "total": 110.0, 
        "fecha": "2026-01-23"
    }
    response = client.post("/api/facturas/", json=factura)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 4
    assert data["reserva_id"] == 4
    
    assert data["total"] == 110.0
    assert data["fecha"] == "2026-01-23"



def test_listar_facturas():
    response = client.get("/api/facturas/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)
    
