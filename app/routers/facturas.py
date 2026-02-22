# Creación de facturas
from fastapi import APIRouter, HTTPException
from app.schemas.factura_schema import FacturaCreate, FacturaResponse, FacturaUpdate

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
    # ✅ orden 1,2,3... (ascendente)
    return sorted(facturas_db, key=lambda x: x["id"])


@router.post("/", response_model=FacturaResponse)
def crear_factura(factura: FacturaCreate):
    # opcional: validar que exista reserva si ya la manejas en memoria
    reserva = _find_by_id(reservas_db, factura.reserva_id)

    nueva = {
        "id": _next_id(facturas_db),
        **factura.model_dump(),
        # ✅ NUEVO campo estado (se calcula por estado de reserva)
        "estado": _estado_factura_por_reserva(reserva),
    }

    facturas_db.append(nueva)
    return nueva


@router.get("/{factura_id}", response_model=FacturaResponse)
def obtener_factura(factura_id: int):
    f = _find_by_id(facturas_db, factura_id)
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

    # ✅ si cambian reserva_id, recalcular estado
    if "reserva_id" in cambios:
        reserva = _find_by_id(reservas_db, cambios["reserva_id"])
        # recalcula estado automáticamente
        actual["estado"] = _estado_factura_por_reserva(reserva)

    # si NO cambió reserva_id, igual conviene recalcular por si reserva cambió
    else:
        reserva = _find_by_id(reservas_db, actual.get("reserva_id"))
        actual["estado"] = _estado_factura_por_reserva(reserva)

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


# =========================
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