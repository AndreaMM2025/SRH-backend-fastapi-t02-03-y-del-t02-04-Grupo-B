# Creación de habitaciones
from fastapi import APIRouter, HTTPException
from app.schemas.habitacion_schema import HabitacionCreate, HabitacionResponse

router = APIRouter(prefix="/api/habitaciones", tags=["Habitaciones"])

habitaciones_db: list[dict] = []

@router.get("/", response_model=list[HabitacionResponse])
def listar_habitaciones():
    return habitaciones_db

@router.post("/", response_model=HabitacionResponse)
def crear_habitacion(habitacion: HabitacionCreate):
    new_id = (max([h["id"] for h in habitaciones_db]) + 1) if habitaciones_db else 1
    nueva = {"id": new_id, **habitacion.model_dump()}
    habitaciones_db.append(nueva)
    return nueva

@router.get("/{habitacion_id}", response_model=HabitacionResponse)
def obtener_habitacion(habitacion_id: int):
    for h in habitaciones_db:
        if h["id"] == habitacion_id:
            return h
    raise HTTPException(status_code=404, detail="Habitación no encontrada")

@router.put("/{habitacion_id}", response_model=HabitacionResponse)
def actualizar_habitacion(habitacion_id: int, habitacion: HabitacionCreate):
    for i, h in enumerate(habitaciones_db):
        if h["id"] == habitacion_id:
            actualizado = {"id": habitacion_id, **habitacion.model_dump()}
            habitaciones_db[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Habitación no encontrada")

@router.delete("/{habitacion_id}")
def eliminar_habitacion(habitacion_id: int):
    for i, h in enumerate(habitaciones_db):
        if h["id"] == habitacion_id:
            habitaciones_db.pop(i)
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Habitación no encontrada")