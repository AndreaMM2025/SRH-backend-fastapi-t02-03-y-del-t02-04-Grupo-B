from fastapi import APIRouter, HTTPException
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate, ReservaResponse


from app.db.memory_db import reservas_db, facturas_db 

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

def _find_by_id(db: list[dict], _id: int):
    return next((x for x in db if x.get("id") == _id), None)

@router.get("/", response_model=list[ReservaResponse])
def listar():
    return reservas_db

@router.post("/", response_model=ReservaResponse)
def crear(data: ReservaCreate):
    nueva = {
        "id": (max([x["id"] for x in reservas_db], default=0) + 1),
        "estado": "pendiente",
        **data.model_dump()
    }
    reservas_db.append(nueva)
    return nueva

@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar(reserva_id: int, data: ReservaUpdate):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    cambios = data.model_dump(exclude_unset=True)

    r.update(cambios)
    return r

@router.put("/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar(reserva_id: int):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    r["estado"] = "confirmada"


    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "emitida"

    return r

@router.put("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar(reserva_id: int):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    r["estado"] = "cancelada"

    # cancelar facturas asociadas
    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "cancelada"

    return r

@router.delete("/{reserva_id}")
def eliminar(reserva_id: int):
    idx = next((i for i, x in enumerate(reservas_db) if x.get("id") == reserva_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    facturas_db[:] = [f for f in facturas_db if f.get("reserva_id") != reserva_id]

    reservas_db.pop(idx)
    return {"ok": True, "message": "Reserva eliminada"}