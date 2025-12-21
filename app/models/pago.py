from typing import Optional
from pydantic import BaseModel
from datetime import date

class Pago(BaseModel):
    id: Optional[int] = None
    factura_id: int
    monto: float
    metodo: str
    fecha: date
