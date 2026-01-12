from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_cliente_1():
    cliente = {
        "nombre": "Andrea Murillo",
        "identificacion": "0954769287",
        "telefono": "0992319870",
        "correo": "amurillom3@est.ups.edu.ec",
        "nacionalidad": "Ecuatoriana"
    }

    response = client.post("/api/clientes/", json=cliente)
    assert response.status_code == 200

    data = response.json()
    assert data["nombre"] == "Andrea Murillo"
    assert data["correo"] == "amurillom3@est.ups.edu.ec"
    assert "id" in data

def test_crear_cliente_2():
    cliente = {
        "nombre": "Andy Arevalo",
        "identificacion": "0950000002",
        "telefono": "0990000002",
        "correo": "david@est.ups.edu.ec",
        "nacionalidad": "Argentina"
    }
    response = client.post("/api/clientes/", json=cliente)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["correo"] == "david@est.ups.edu.ec"
    assert "id" in data

def test_crear_cliente_3():
    cliente = {
        "nombre": "Kevin Ramírez",
        "identificacion": "0989567895",
        "telefono": "0993467859",
        "correo": "kevin3@est.ups.edu.ec",
        "nacionalidad": "Colombiana"
    }
    response = client.post("/api/clientes/", json=cliente)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data ["correo"] == "kevin3@est.ups.edu.ec"
    assert "id" in data

def test_listar_clientes():
    response = client.get("/api/clientes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
