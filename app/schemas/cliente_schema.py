# Creación de ClienteCreate y ClienteResponse
from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str
    identidad: str
    nacionalidad: str

class ClienteResponse(ClienteCreate):
    id: int
