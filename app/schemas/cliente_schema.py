from typing import Optional
from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    identificacion: str
    telefono: str
    correo: EmailStr
    nacionalidad: str

class ClienteOut(ClienteCreate):
    id: int