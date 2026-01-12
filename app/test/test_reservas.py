from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crear_reserva_1():
    reserva = {
        "cliente_id": 1,
        "habitacion_id": 1,
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-01-05"
    }

    response = client.post("/api/reservas/", json=reserva)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 1
    assert data["habitacion_id"] == 1
    assert "id" in data
    assert "estado" in data


def test_confirmar_reserva_1():
    reserva = {
        "cliente_id": 1,
        "habitacion_id": 1,
        "fecha_inicio": "2025-02-01",
        "fecha_fin": "2025-02-05"
    }

    r_create = client.post("/api/reservas/", json=reserva)
    assert r_create.status_code == 200, r_create.text
    reserva_id = r_create.json()["id"]

    r_confirm = client.put(f"/api/reservas/{reserva_id}/confirmar")
    assert r_confirm.status_code == 200, r_confirm.text

    data = r_confirm.json()
    assert data["id"] == reserva_id
    assert "estado" in data


def test_cancelar_reserva_1():
    reserva = {
        "cliente_id": 1,
        "habitacion_id": 1,
        "fecha_inicio": "2025-03-01",
        "fecha_fin": "2025-03-05"
    }

    r_create = client.post("/api/reservas/", json=reserva)
    assert r_create.status_code == 200, r_create.text
    reserva_id = r_create.json()["id"]

    r_cancel = client.put(f"/api/reservas/{reserva_id}/cancelar")
    assert r_cancel.status_code == 200, r_cancel.text

    data = r_cancel.json()
    assert data["id"] == reserva_id
    assert "estado" in data

def test_crear_reserva_2():
    reserva = {
        "cliente_id": 2,
        "habitacion_id": 2,
        "fecha_inicio": "2025-02-05",
        "fecha_fin": "2025-02-10"
    }

    response = client.post("/api/reservas/", json=reserva)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["cliente_id"] == 2
    assert data["habitacion_id"] == 2
    assert "id" in data
    assert "estado" in data

    response = client.post("/api/reservas/", json=reserva)
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["cliente_id"] == 2
    assert data["habitacion_id"] == 2
    assert "id" in data
    assert "estado" in data

def test_confirmar_reserva_2():
    reserva = {
        "cliente_id": 2,
        "habitacion_id": 2,
        "fecha_inicio": "2025-02-05",
        "fecha_fin": "2025-02-10"
    }
    r_create = client.post("/api/reservas/", json=reserva)
    assert r_create.status_code == 200, r_create.text
    reserva_id = r_create.json()["id"]

    r_confirm = client.put(f"/api/reservas/{reserva_id}/confirmar")
    assert r_confirm.status_code == 200, r_confirm.text

    data = r_confirm.json()
    assert data["id"] == reserva_id
    assert "estado" in data


def test_cancelar_reserva_2():
    reserva = {
        "cliente_id": 2,
        "habitacion_id": 2,
        "fecha_inicio": "2025-02-05",
        "fecha_fin": "2025-02-10"
    }

    r_create = client.post("/api/reservas/", json=reserva)
    assert r_create.status_code == 200, r_create.text
    reserva_id = r_create.json()["id"]

    r_cancel = client.put(f"/api/reservas/{reserva_id}/cancelar")
    assert r_cancel.status_code == 200, r_cancel.text

    data = r_cancel.json()
    assert data["id"] == reserva_id
    assert "estado" in data

def test_crear_reserva_3():
    reserva = {
        "cliente_id": 3,
        "habitacion_id": 3,
        "fecha_inicio": "2025-05-20",
        "fecha_fin": "2025-05-25"
    }
    response = client.post("/api/reservas/", json=reserva)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["cliente_id"] == 3
    global reserva_id_3
    reserva_id_3 = data["id"]

def test_confirmar_reserva_3():
    reserva = {
        "cliente_id": 3,
        "habitacion_id": 3,
        "fecha_inicio": "2025-05-20",
        "fecha_fin": "2025-05-25"
    }
    response = client.put(f"/api/reservas/{reserva_id_3}/confirmar")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == reserva_id_3
    assert data["estado"] == "confirmada"

def test_cancelar_reserva_3():
    reserva = {
        "cliente_id": 3,
        "habitacion_id": 3,
        "fecha_inicio": "2025-05-20",
        "fecha_fin": "2025-05-25"
    }
    response = client.put(f"/api/reservas/{reserva_id_3}/cancelar")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == reserva_id_3
    assert data["estado"] == "cancelada"

def test_confirmar_reserva_inexistente():
    response = client.put("/api/reservas/999999/confirmar")
    assert response.status_code == 404, response.text


def test_cancelar_reserva_inexistente():
    response = client.put("/api/reservas/999999/cancelar")
    assert response.status_code == 404, response.text

def test_listar_reservas():
    response = client.get("/api/reservas/")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)

