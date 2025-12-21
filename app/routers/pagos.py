from fastapi import APIRouter
from app.schemas.pago_schema import PagoCreate, PagoResponse

router = APIRouter(
    prefix="/api/pagos",
    tags=["Pagos"]
)

# Base de datos en memoria
pagos_db: list[dict] = []

@router.get("/", response_model=list[PagoResponse])
def listar_pagos():
    return pagos_db

@router.post("/", response_model=PagoResponse)
def crear_pago(pago: PagoCreate):
    nuevo = {
        "id": len(pagos_db) + 1,
        **pago.model_dump()
    }
    pagos_db.append(nuevo)
    return nuevo
