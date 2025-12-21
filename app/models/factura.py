from typing import Optional
from pydantic import BaseModel
from datetime import date

class Factura(BaseModel):
    id: Optional[int] = None
    cliente_id: int
    reserva_id: int
    total: float
    fecha: date
