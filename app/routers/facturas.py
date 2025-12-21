from fastapi import APIRouter
from app.schemas.factura_schema import FacturaCreate, FacturaResponse

router = APIRouter(
    prefix="/api/facturas",
    tags=["Facturas"]
)

# Base de datos en memoria
facturas_db: list[dict] = []

@router.get("/", response_model=list[FacturaResponse])
def listar_facturas():
    return facturas_db

@router.post("/", response_model=FacturaResponse)
def crear_factura(factura: FacturaCreate):
    nueva = {
        "id": len(facturas_db) + 1,
        **factura.model_dump()
    }
    facturas_db.append(nueva)
    return nueva
