from fastapi import APIRouter, HTTPException
from app.schemas.reserva_schema import ReservaCreate, ReservaUpdate, ReservaResponse
from app.db.memory_db import reservas_db, facturas_db, pagos_db
from datetime import datetime

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

def _find_by_id(db: list[dict], _id: int):
    return next((x for x in db if x.get("id") == _id), None)

# VALIDACIÓN: Verificar si hay fechas solapadas
def _fechas_solapan(inicio1: str, fin1: str, inicio2: str, fin2: str) -> bool:
    """Retorna True si las fechas se solapan"""
    return inicio1 < fin2 and fin1 > inicio2

#  VALIDACIÓN: Verificar si el cliente ya tiene reserva activa en ese período
def _validar_reserva_duplicada(cliente_id: int, fecha_inicio: str, fecha_fin: str, reserva_id: int = None):
    """
    Valida que el cliente no tenga otra reserva activa con fechas solapadas.
    - reserva_id: Si se proporciona, se excluye esa reserva (para actualizaciones)
    """ 
    for r in reservas_db:
        # Excluir la misma reserva (para actualizaciones)
        if reserva_id and r.get("id") == reserva_id:
            continue
        
        # Solo verificar reservas activas (no canceladas)
        if r.get("estado") == "cancelada":
            continue
        
        # Verificar si es del mismo cliente
        if r.get("cliente_id") != cliente_id:
            continue
        
        # Verificar si las fechas se solapan
        if _fechas_solapan(fecha_inicio, fecha_fin, r.get("fecha_inicio", ""), r.get("fecha_fin", "")):
            raise HTTPException(
                status_code=400, 
                detail=f"El cliente ya tiene una reserva activa (#{r.get('id')}) en el período {r.get('fecha_inicio')} a {r.get('fecha_fin')}"
            )

@router.get("/", response_model=list[ReservaResponse])
def listar():
    return reservas_db

@router.post("/", response_model=ReservaResponse)
def crear(data: ReservaCreate):
    # ✅ VALIDAR: No permitir reservas duplicadas
    _validar_reserva_duplicada(
        cliente_id=data.cliente_id,
        fecha_inicio=data.fecha_inicio,
        fecha_fin=data.fecha_fin,
        reserva_id=None
    )
    
    nueva = {
        "id": (max([x["id"] for x in reservas_db], default=0) + 1),
        "estado": "pendiente",
        **data.model_dump()
    }
    reservas_db.append(nueva)
    return nueva

@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar(reserva_id: int, data: ReservaUpdate):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    cambios = data.model_dump(exclude_unset=True)
    
    # ✅ VALIDAR: Si se están cambiando fechas o cliente, verificar duplicados
    cliente_id = cambios.get("cliente_id", r.get("cliente_id"))
    fecha_inicio = cambios.get("fecha_inicio", r.get("fecha_inicio"))
    fecha_fin = cambios.get("fecha_fin", r.get("fecha_fin"))
    
    _validar_reserva_duplicada(
        cliente_id=cliente_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        reserva_id=reserva_id  # ✅ Excluir esta reserva de la validación
    )

    r.update(cambios)
    return r

@router.put("/{reserva_id}/confirmar", response_model=ReservaResponse)
def confirmar(reserva_id: int):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    r["estado"] = "confirmada"

    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "emitida"
            for p in pagos_db:
                if p.get("factura_id") == f.get("id"):
                    p["estado"] = "aprobado"

    return r

@router.put("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar(reserva_id: int):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    r["estado"] = "cancelada"

    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "cancelada"
            for p in pagos_db:
                if p.get("factura_id") == f.get("id"):
                    p["estado"] = "anulado"

    return r

@router.delete("/{reserva_id}")
def eliminar(reserva_id: int):
    idx = next((i for i, x in enumerate(reservas_db) if x.get("id") == reserva_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    facturas_db[:] = [f for f in facturas_db if f.get("reserva_id") != reserva_id]
    reservas_db.pop(idx)
    return {"ok": True, "message": "Reserva eliminada"}