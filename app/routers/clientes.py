# Creación de clientes
from fastapi import APIRouter, HTTPException, Query
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse
from app.db.memory import clientes_db, reservas_db, facturas_db

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
    # 1) verificar cliente existe
    idx = next((i for i, c in enumerate(clientes_db) if c["id"] == cliente_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2) obtener reservas del cliente
    reserva_ids = [r["id"] for r in reservas_db if r.get("cliente_id") == cliente_id]

    # 3) borrar facturas asociadas a esas reservas o al cliente
    # (por seguridad: por reserva_id y por cliente_id)
    facturas_antes = len(facturas_db)
    facturas_db[:] = [
        f for f in facturas_db
        if (f.get("cliente_id") != cliente_id) and (f.get("reserva_id") not in reserva_ids)
    ]
    facturas_borradas = facturas_antes - len(facturas_db)

    # 4) borrar reservas del cliente
    reservas_antes = len(reservas_db)
    reservas_db[:] = [r for r in reservas_db if r.get("cliente_id") != cliente_id]
    reservas_borradas = reservas_antes - len(reservas_db)

    # 5) borrar cliente
    clientes_db.pop(idx)

    return {
        "ok": True,
        "message": "Cliente eliminado con cascada",
        "cliente_id": cliente_id,
        "reservas_eliminadas": reservas_borradas,
        "facturas_eliminadas": facturas_borradas,
    }