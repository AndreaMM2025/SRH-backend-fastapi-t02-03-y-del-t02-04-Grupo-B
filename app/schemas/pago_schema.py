# app/schemas/pago_schema.py

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PagoBase(BaseModel):
    factura_id: int = Field(..., ge=1)
    monto: float = Field(..., ge=0)
    metodo: str = Field(..., min_length=1)
    fecha: date

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    factura_id: Optional[int] = Field(None, ge=1)
    monto: Optional[float] = Field(None, ge=0)
    metodo: Optional[str] = Field(None, min_length=1)
    fecha: Optional[date] = None

class PagoResponse(PagoBase):
    id: int