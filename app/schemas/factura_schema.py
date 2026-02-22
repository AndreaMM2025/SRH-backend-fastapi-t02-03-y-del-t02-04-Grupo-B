from pydantic import BaseModel
from typing import Optional
from datetime import date

class FacturaCreate(BaseModel):
    cliente_id: int
    reserva_id: int
    total: float
    fecha: date

class FacturaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    reserva_id: Optional[int] = None
    total: Optional[float] = None
    fecha: Optional[date] = None
    estado: Optional[str] = None

class FacturaResponse(BaseModel):
    id: int
    cliente_id: int
    reserva_id: int
    total: float
    fecha: date
    estado: str