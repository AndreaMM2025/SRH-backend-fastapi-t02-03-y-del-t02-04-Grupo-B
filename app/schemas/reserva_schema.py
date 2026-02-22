# Creación de ReservaCreate y ReservaResponse
from pydantic import BaseModel
from typing import Optional

class ReservaCreate(BaseModel):
    cliente_id: int
    habitacion_id: int
    fecha_inicio: str
    fecha_fin: str

class ReservaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    habitacion_id: Optional[int] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None
    estado: Optional[str] = None

class ReservaResponse(ReservaCreate):
    id: int
    estado: str