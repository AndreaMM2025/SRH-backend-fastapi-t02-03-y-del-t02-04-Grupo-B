# Creación de clientes
from fastapi import APIRouter
from app.schemas.cliente_schema import ClienteCreate, ClienteResponse

router = APIRouter(
    prefix="/api/clientes",
    tags=["Clientes"]
)

# Base de datos en memoria
clientes_db: list[dict] = []

@router.get("/", response_model=list[ClienteResponse])
def listar_clientes():
    return clientes_db

@router.post("/", response_model=ClienteResponse)
def crear_cliente(cliente: ClienteCreate):
    nuevo = {
        "id": len(clientes_db) + 1,
        **cliente.model_dump()
    }
    clientes_db.append(nuevo)
    return nuevo
