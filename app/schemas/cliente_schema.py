# Creación de ClienteCreate y ClienteResponse
from pydantic import BaseModel, EmailStr

class ClienteCreate(BaseModel):
    nombre: str
    identificacion: str
    telefono: str
    correo: EmailStr
    nacionalidad: str

class ClienteResponse(ClienteCreate):
    id: int