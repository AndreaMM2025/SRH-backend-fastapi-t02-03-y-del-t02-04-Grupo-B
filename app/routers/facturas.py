from fastapi import APIRouter, HTTPException
from app.db.memory_db import facturas_db, reservas_db, next_id, find_by_id

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])

@router.get("/")
def listar_facturas():
    return facturas_db

@router.post("/")
def crear_factura(data: dict):
    # estado por defecto depende de reserva si existe
    reserva_id = data.get("reserva_id")
    estado = data.get("estado")

    if not estado:
        r = next((x for x in reservas_db if x.get("id") == reserva_id), None)
        if r and (r.get("estado") or "").lower() == "cancelada":
            estado = "cancelada"
        elif r and (r.get("estado") or "").lower() == "confirmada":
            estado = "emitida"
        else:
            estado = "pendiente"

    nueva = {"id": next_id(facturas_db), **data, "estado": estado}
    facturas_db.append(nueva)
    return nueva

@router.put("/{factura_id}")
def actualizar_factura(factura_id: int, data: dict):
    f = find_by_id(facturas_db, factura_id)
    if not f:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    f.update(data)

    reserva_id = f.get("reserva_id")
    r = next((x for x in reservas_db if x.get("id") == reserva_id), None)
    if r and (r.get("estado") or "").lower() == "cancelada":
        f["estado"] = "cancelada"

    return f

@router.delete("/{factura_id}")
def eliminar_factura(factura_id: int):
    f = find_by_id(facturas_db, factura_id)
    if not f:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    facturas_db[:] = [x for x in facturas_db if x.get("id") != factura_id]
    return {"ok": True, "message": "Factura eliminada"}