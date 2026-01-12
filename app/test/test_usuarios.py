from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_usuario_1():
    usuario = {
        "nombre": "Admin",
        "rol": "administrador",
        "estado": True
    }

    response = client.post("/api/usuarios/", json=usuario)
    assert response.status_code == 200

    data = response.json()

    # Validamos campos principales
    assert data["nombre"] == "Admin"
    assert data["rol"] == "administrador"
    assert data["estado"] is True

    # Validamos que el backend genere un id
    assert "id" in data

def test_crear_usuario_2():
    usuario = {
        "nombre": "David",
        "rol": "Recepcionista",
        "estado": True
    }

    response = client.post("/api/usuarios/", json=usuario)
    assert response.status_code == 200

    data = response.json()

    # Validamos campos principales
    assert data["nombre"] == "David"
    assert data["rol"] == "Recepcionista"
    assert data["estado"] is True

    # Validamos que el backend genere un id
    assert "id" in data

def test_crear_usuario_3():
    usuario = {
        "nombre": "Kevin",
        "rol": "Supervisor",
        "estado": True
    }

    response = client.post("/api/usuarios/", json=usuario)
    assert response.status_code == 200

    data = response.json()

    # Validamos campos principales
    assert data["nombre"] == "Andres"
    assert data["rol"] == "Supervisor"
    assert data["estado"] is True

    # Validamos que el backend genere un id
    assert "id" in data

def test_listar_usuarios():
    response = client.get("/api/usuarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
