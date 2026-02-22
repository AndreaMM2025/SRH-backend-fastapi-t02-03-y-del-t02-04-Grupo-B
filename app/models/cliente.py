# Modelo: Cliente
from typing import Optional
from pydantic import BaseModel, EmailStr

class Cliente(BaseModel):
    id: Optional[int] = None
    nombre: str
    identidad: str
    telefono: str
    correo: EmailStr
    nacionalidad: str
