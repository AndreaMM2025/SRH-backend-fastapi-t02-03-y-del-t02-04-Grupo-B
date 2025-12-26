# Modelo Habitacion
from typing import Optional
from pydantic import BaseModel

class Habitacion(BaseModel):
    id: Optional[int] = None
    numero: str
    tipo: str
    tarifa: float
    estado: str = "Disponible"
