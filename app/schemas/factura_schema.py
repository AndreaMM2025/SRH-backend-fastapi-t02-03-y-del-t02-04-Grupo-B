from pydantic import BaseModel
from datetime import date

class FacturaCreate(BaseModel):
    cliente_id: int
    reserva_id: int
    total: float
    fecha: date

class FacturaResponse(FacturaCreate):
    id: int
    
class FacturaUpdate(BaseModel):
    cliente_id: int | None = None
    reserva_id: int | None = None
    total: float | None = None
    fecha: date | None = None