from pydantic import BaseModel

class ReservaCreate(BaseModel):
    cliente_id: int
    habitacion_id: int
    fecha_inicio: str
    fecha_fin: str

class ReservaResponse(ReservaCreate):
    id: int
    estado: str
