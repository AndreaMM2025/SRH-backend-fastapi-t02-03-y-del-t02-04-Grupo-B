#  Endpoints reservas con estados
from fastapi import APIRouter, HTTPException
from app.schemas.reserva_schema import ReservaCreate, ReservaResponse
from app.db.memory_db import reservas_db, facturas_db, clientes_db

router = APIRouter(
    prefix="/api/reservas",
    tags=["Reservas"]
)


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas():
    return reservas_db

@router.post("/", response_model=ReservaResponse)
def crear_reserva(reserva: ReservaCreate):
    nueva = {
        "id": len(reservas_db) + 1,
        **reserva.model_dump(),
        "estado": "pendiente"
    }
    reservas_db.append(nueva)
    return nueva

@router.put("/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar_reserva(reserva_id: int):
    for r in reservas_db:
        if r["id"] == reserva_id:
            r["estado"] = "confirmada"
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@router.put("/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: int):
    r = next((x for x in reservas_db if x["id"] == reserva_id), None)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    r["estado"] = "cancelada"
    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "cancelada"

    return {"ok": True, "reserva": r}

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