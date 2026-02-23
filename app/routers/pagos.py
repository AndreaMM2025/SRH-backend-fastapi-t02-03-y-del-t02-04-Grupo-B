# app/routers/pagos.py

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

    # validar que exista la factura
    f = find_by_id(facturas_db, int(factura_id))
    if not f:
        raise HTTPException(status_code=400, detail="Factura no existe")

    # estado por defecto (si no viene)
    estado = data.get("estado")
    if not estado:
        # Si la factura está cancelada -> pago anulado
        if (f.get("estado") or "").lower() == "cancelada":
            estado = "anulado"
        else:
            estado = "aprobado"

    nueva = {"id": next_id(pagos_db), **data, "estado": estado}
    pagos_db.append(nueva)
    return nueva


@router.put("/{pago_id}")
def actualizar_pago(pago_id: int, data: dict):
    p = find_by_id(pagos_db, pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    # si cambian factura_id -> validar
    if "factura_id" in data and data["factura_id"] is not None:
        f = find_by_id(facturas_db, int(data["factura_id"]))
        if not f:
            raise HTTPException(status_code=400, detail="Factura no existe")

        # si la factura está cancelada, el pago debe quedar anulado
        if (f.get("estado") or "").lower() == "cancelada":
            data["estado"] = "anulado"

    # aplicar cambios
    p.update(data)

    # regla extra: si la factura asociada está cancelada -> pago anulado
    f2 = find_by_id(facturas_db, int(p.get("factura_id", 0))) if p.get("factura_id") else None
    if f2 and (f2.get("estado") or "").lower() == "cancelada":
        p["estado"] = "anulado"

    return p


@router.delete("/{pago_id}")
def eliminar_pago(pago_id: int):
    p = find_by_id(pagos_db, pago_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    pagos_db[:] = [x for x in pagos_db if x.get("id") != pago_id]
    return {"ok": True, "message": "Pago eliminado"}