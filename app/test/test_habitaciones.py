from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_habitacion_1():
    habitacion = {
        "numero": "101",
        "tipo": "Simple",
        "precio": 50.0,
        "disponible": True
    }

    response = client.post("/api/habitaciones/", json=habitacion)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["numero"] == "101"
    assert data["tipo"] == "Simple"
    assert data["precio"] == 50.0
    assert data["disponible"] is True

def test_crear_habitacion_2():
    habitacion = {
        "numero": "102",
        "tipo": "Doble",
        "precio": 100.0,
        "disponible": True
    }

    response = client.post("/api/habitaciones/", json=habitacion)
    
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["numero"] == "102"
    assert data["tipo"] == "Doble"
    assert data["precio"] == 100.0
    assert data["disponible"] is True

def test_listar_habitaciones():
    response = client.get("/api/habitaciones/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)
