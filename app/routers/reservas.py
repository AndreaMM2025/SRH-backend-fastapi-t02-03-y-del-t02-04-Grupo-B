from fastapi import APIRouter, HTTPException
from app.schemas.reserva_schema import ReservaCreate, ReservaResponse

router = APIRouter(
    prefix="/api/reservas",
    tags=["Reservas"]
)

# Base de datos en memoria
reservas_db: list[dict] = []

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

@router.put("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(reserva_id: int):
    for r in reservas_db:
        if r["id"] == reserva_id:
            r["estado"] = "cancelada"
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")
