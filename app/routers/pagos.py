# app/routers/pagos.py creacion de pagos y estado

from fastapi import APIRouter, HTTPException
from app.db.memory_db import pagos_db, facturas_db, next_id, find_by_id, delete_by_id
router = APIRouter(prefix="/api/pagos", tags=["Pagos"])

@router.get("/")
def listar_pagos():
    return pagos_db


@router.post("/")
def crear_pago(data: dict):
    """
    data esperado (ejemplo):
    {
      "factura_id": 1,
      "monto": 50,
      "metodo": "efectivo" | "debito" | "tarjeta-mastercard" | "tarjeta-visa" | "transferencia" | "otro",
      "fecha": "2026-02-22",
      "estado": "aprobado" (opcional)
    }
    """
    factura_id = data.get("factura_id")
    if not factura_id:
        raise HTTPException(status_code=400, detail="factura_id es requerido")

    f = find_by_id(facturas_db, int(factura_id))
    if not f:
        raise HTTPException(status_code=400, detail="Factura no existe")

    estado = data.get("estado")
    if not estado:
        est_fact = (f.get("estado") or "").lower()
        if est_fact == "cancelada":
            estado = "anulado"
        elif est_fact == "pendiente":
            estado = "pendiente"
        else:  # emitida
            estado = "aprobado"

    nueva = {"id": next_id(pagos_db), **data, "estado": estado}
    pagos_db.append(nueva)
    return nueva

@router.put("/{pago_id}")
def actualizar_pago(pago_id: int, data: dict):
    p = find_by_id(pagos_db, pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    if "factura_id" in data and data["factura_id"] is not None:
        f = find_by_id(facturas_db, int(data["factura_id"]))
        if not f:
            raise HTTPException(status_code=400, detail="Factura no existe")

    p.update(data)

    f2 = find_by_id(facturas_db, int(p.get("factura_id", 0))) if p.get("factura_id") else None
    if f2:
        est_fact = (f2.get("estado") or "").lower()
        if est_fact == "cancelada":
            p["estado"] = "anulado"
        elif est_fact == "pendiente":
            p["estado"] = "pendiente"
        else:
            p["estado"] = "aprobado"

    return p


@router.delete("/{pago_id}")
def eliminar_pago(pago_id: int):
    p = find_by_id(pagos_db, pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pagos_db[:] = [x for x in pagos_db if x.get("id") != pago_id]
    return {"ok": True, "message": "Pago eliminado"}