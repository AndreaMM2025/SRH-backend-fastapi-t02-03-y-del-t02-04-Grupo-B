from typing import Optional
from pydantic import BaseModel

class Habitacion(BaseModel):
    id: Optional[int] = None
    numero: str
    tipo: str
    precio: float
    disponible: bool = True
