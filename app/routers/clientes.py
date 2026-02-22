from fastapi import APIRouter, HTTPException
from app.db.memory_db import clientes_db, reservas_db, facturas_db, find_by_id

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes():
    return clientes_db

@router.post("/")
def crear_cliente(data: dict):
    from app.db.memory_db import next_id
    nuevo = {"id": next_id(clientes_db), **data}
    clientes_db.append(nuevo)
    return nuevo

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    c = find_by_id(clientes_db, cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 1) obtener reservas del cliente
    reservas_a_borrar = [r for r in reservas_db if r.get("cliente_id") == cliente_id]
    reserva_ids = {r["id"] for r in reservas_a_borrar}

    # 2) borrar facturas asociadas a esas reservas (o por cliente_id si lo guardas)
    facturas_db[:] = [
        f for f in facturas_db
        if f.get("reserva_id") not in reserva_ids and f.get("cliente_id") != cliente_id
    ]

    # 3) borrar reservas del cliente
    reservas_db[:] = [r for r in reservas_db if r.get("cliente_id") != cliente_id]

    # 4) borrar cliente
    clientes_db[:] = [x for x in clientes_db if x.get("id") != cliente_id]

    return {"ok": True, "message": "Cliente eliminado"}

@router.put("/{cliente_id}")  # ← AGREGA ESTO
def actualizar_cliente(cliente_id: int, data: dict):
    cliente = find_by_id(clientes_db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Actualizar solo los campos que vienen en data
    cliente.update(data)
    return cliente