from pydantic import BaseModel
from datetime import date

class FacturaCreate(BaseModel):
    cliente_id: int
    reserva_id: int
    total: float
    fecha: date

class FacturaResponse(FacturaCreate):
    id: int
