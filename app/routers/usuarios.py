# Creación de usuarios
from fastapi import APIRouter
from app.models.usuario import Usuario

router = APIRouter(
    prefix="/api/usuarios",
    tags=["usuarios"]
)

# Base de datos en memoria
usuarios_db: list[dict] = []

@router.get("/", response_model=list[Usuario])
def listar_usuarios():
    return usuarios_db

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: Usuario):
    nuevo = {
        "id": len(usuarios_db) + 1,
        **usuario.model_dump(exclude={"id"})
    }
    usuarios_db.append(nuevo)
    return nuevo
