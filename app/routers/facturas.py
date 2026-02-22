# Creación de facturas
from fastapi import APIRouter, HTTPException
from app.schemas.factura_schema import FacturaCreate, FacturaResponse, FacturaUpdate

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
        "id": (max([f["id"] for f in facturas_db], default=0) + 1),
        **factura.model_dump()
    }
    facturas_db.append(nueva)
    return nueva

@router.get("/{factura_id}", response_model=FacturaResponse)
def obtener_factura(factura_id: int):
    f = next((x for x in facturas_db if x["id"] == factura_id), None)
    if not f:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return f


@router.put("/{factura_id}", response_model=FacturaResponse)
def actualizar_factura(factura_id: int, data: FacturaUpdate):
    idx = next((i for i, x in enumerate(facturas_db) if x["id"] == factura_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    actual = facturas_db[idx]
    cambios = data.model_dump(exclude_unset=True)

    actual.update(cambios)
    facturas_db[idx] = actual
    return actual


@router.delete("/{factura_id}")
def eliminar_factura(factura_id: int):
    idx = next((i for i, x in enumerate(facturas_db) if x["id"] == factura_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    facturas_db.pop(idx)
    return {"ok": True, "message": "Factura eliminada"}