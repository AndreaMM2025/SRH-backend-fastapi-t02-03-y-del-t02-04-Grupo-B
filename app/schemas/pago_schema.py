from pydantic import BaseModel
from datetime import date

class PagoCreate(BaseModel):
    factura_id: int
    monto: float
    metodo: str
    fecha: date

class PagoResponse(PagoCreate):
    id: int
