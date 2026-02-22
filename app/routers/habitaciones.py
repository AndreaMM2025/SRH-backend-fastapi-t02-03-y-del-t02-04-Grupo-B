# Creación de habitaciones
from fastapi import APIRouter, HTTPException
from app.schemas.habitacion_schema import HabitacionCreate, HabitacionResponse

router = APIRouter(
    prefix="/api/habitaciones",
    tags=["Habitaciones"]
)

# "DB" en memoria
habitaciones_db: list[dict] = []
_next_id = 1


def _find_index(habitacion_id: int) -> int:
    for i, h in enumerate(habitaciones_db):
        if h["id"] == habitacion_id:
            return i
    return -1


@router.get("", response_model=list[HabitacionResponse])
def listar_habitaciones():
    return habitaciones_db


@router.post("", response_model=HabitacionResponse)
def crear_habitacion(habitacion: HabitacionCreate):
    global _next_id
    nueva = {
        "id": _next_id,
        **habitacion.model_dump()
    }
    _next_id += 1
    habitaciones_db.append(nueva)
    return nueva


@router.get("/{habitacion_id}", response_model=HabitacionResponse)
def obtener_habitacion(habitacion_id: int):
    idx = _find_index(habitacion_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitaciones_db[idx]


@router.put("/{habitacion_id}", response_model=HabitacionResponse)
def actualizar_habitacion(habitacion_id: int, habitacion: HabitacionCreate):
    idx = _find_index(habitacion_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    actualizado = {
        "id": habitacion_id,
        **habitacion.model_dump()
    }
    habitaciones_db[idx] = actualizado
    return actualizado


@router.delete("/{habitacion_id}")
def eliminar_habitacion(habitacion_id: int):
    idx = _find_index(habitacion_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")

    habitaciones_db.pop(idx)
    return {"message": "Habitación eliminada"}