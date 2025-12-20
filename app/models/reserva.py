from typing import Optional
from pydantic import BaseModel

class Reserva(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    habitacion_id: int
    fecha_inicio: str
    fecha_fin: str
    estado: str = "pendiente"  # pendiente | confirmada | cancelada
