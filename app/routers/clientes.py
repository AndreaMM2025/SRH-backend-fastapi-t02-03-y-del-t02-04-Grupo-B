# Creación de clientes
from fastapi import APIRouter, HTTPException, Query
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse

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
    for i, c in enumerate(clientes_db):
        if c["id"] == cliente_id:
            clientes_db.pop(i)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")