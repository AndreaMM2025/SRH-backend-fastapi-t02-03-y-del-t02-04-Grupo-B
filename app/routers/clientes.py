# Creación de clientes
from fastapi import APIRouter, HTTPException, Query
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse
from app.db.memory_db import clientes_db, reservas_db, facturas_db

router = APIRouter(
    prefix="/api/clientes",
    tags=["Clientes"]
)

clientes_db: list[dict] = []

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(q: str | None = Query(default=None)):
    if not q:
        return clientes_db

    ql = q.lower().strip()
    return [
        c for c in clientes_db
        if ql in str(c.get("nombre", "")).lower()
        or ql in str(c.get("identificacion", "")).lower()
        or ql in str(c.get("telefono", "")).lower()
        or ql in str(c.get("correo", "")).lower()
        or ql in str(c.get("nacionalidad", "")).lower()
    ]

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int):
    for c in clientes_db:
        if c["id"] == cliente_id:
            return c
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate):
    nuevo = {"id": len(clientes_db) + 1, **cliente.model_dump()}
    clientes_db.append(nuevo)
    return nuevo

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente: ClienteCreate):
    for i, c in enumerate(clientes_db):
        if c["id"] == cliente_id:
            actualizado = {"id": cliente_id, **cliente.model_dump()}
            clientes_db[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    # 1) buscar cliente
    idx = next((i for i, c in enumerate(clientes_db) if c["id"] == cliente_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2) sacar reservas del cliente (guardar ids)
    reservas_del_cliente = [r for r in reservas_db if r.get("cliente_id") == cliente_id]
    ids_reservas = {r["id"] for r in reservas_del_cliente}

    # 3) eliminar reservas del cliente
    reservas_db[:] = [r for r in reservas_db if r.get("cliente_id") != cliente_id]

    # 4) eliminar facturas del cliente + facturas por reserva (por si acaso)
    facturas_db[:] = [
        f for f in facturas_db
        if f.get("cliente_id") != cliente_id and f.get("reserva_id") not in ids_reservas
    ]

    # 5) eliminar cliente
    clientes_db.pop(idx)

    return {
        "ok": True,
        "message": "Cliente eliminado con reservas y facturas asociadas",
        "reservas_eliminadas": len(ids_reservas),
    }