# Creación de facturas
from fastapi import APIRouter, HTTPException
from app.schemas.factura_schema import FacturaCreate, FacturaResponse, FacturaUpdate
from app.db.memory import facturas_db, reservas_db, next_id

router = APIRouter(prefix="/api/facturas", tags=["Facturas"])

# =========================
# "DB" EN MEMORIA
# =========================
facturas_db: list[dict] = []
reservas_db: list[dict] = []  


# =========================
# HELPERS
# =========================
def _next_id(db: list[dict]) -> int:
    return max((x["id"] for x in db), default=0) + 1

def _find_by_id(db: list[dict], _id: int):
    return next((x for x in db if x["id"] == _id), None)

def _estado_factura_por_reserva(reserva: dict | None) -> str:
    """
    Reglas:
    - si la reserva está cancelada -> factura cancelada
    - si la reserva está confirmada -> factura emitida
    - si la reserva está pendiente -> factura pendiente
    """
    if not reserva:
        return "pendiente"

    est = (reserva.get("estado") or "").lower()
    if "cancel" in est:
        return "cancelada"
    if "confirm" in est:
        return "emitida"
    return "pendiente"


# =========================
# CRUD FACTURAS
# =========================
@router.get("/", response_model=list[FacturaResponse])
def listar_facturas():
    return facturas_db

@router.post("/", response_model=FacturaResponse)
def crear_factura(factura: FacturaCreate):
    # Estado depende de la reserva (si existe)
    estado = "pendiente"
    r = next((x for x in reservas_db if x["id"] == factura.reserva_id), None)
    if r:
        est = (r.get("estado") or "").lower()
        if "cancel" in est:
            estado = "cancelada"
        elif "confirm" in est:
            estado = "emitida"

    nueva = {
        "id": next_id(facturas_db),
        **factura.model_dump(),
        "estado": estado,
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

# x 
# CANCELAR RESERVA (EN MEMORIA)
# =========================
@router.put("/reservas/{reserva_id}/cancelar")
def cancelar_reserva(reserva_id: int):
    r = _find_by_id(reservas_db, reserva_id)
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    # 1) cancelar reserva
    r["estado"] = "cancelada"

    # 2) cancelar factura(s) asociada(s)
    for f in facturas_db:
        if f.get("reserva_id") == reserva_id:
            f["estado"] = "cancelada"

    return {"ok": True, "message": "Reserva cancelada y facturas asociadas canceladas"}