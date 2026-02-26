from fastapi import APIRouter
from typing import Optional
from datetime import datetime

from app.db.memory_db import (
    clientes_db,
    reservas_db,
    habitaciones_db,
    facturas_db,
    pagos_db
)

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])


# ============================================================
# REPORTE DE INGRESOS
# ============================================================
@router.get("/ingresos")
def reporte_ingresos(fecha_inicio: Optional[str] = None, fecha_fin: Optional[str] = None):
    pagos_filtrados = pagos_db

    if fecha_inicio:
        pagos_filtrados = [p for p in pagos_filtrados if (p.get("fecha", "") >= fecha_inicio)]
    if fecha_fin:
        pagos_filtrados = [p for p in pagos_filtrados if (p.get("fecha", "") <= fecha_fin)]

    total_aprobado = 0.0
    total_iva_aprobado = 0.0
    total_por_cobrar = 0.0
    total_anulado = 0.0

    c_aprobado = 0
    c_pendiente = 0
    c_anulado = 0

    factura_ids_aprobadas = set()

    for p in pagos_filtrados:
        monto = float(p.get("monto", 0) or 0)
        iva = p.get("iva")
        iva = round(monto * 0.15, 2) if iva is None else float(iva or 0)
        est = (p.get("estado") or "").lower()

        if est == "aprobado":
            c_aprobado += 1
            total_iva_aprobado += iva
            total_aprobado += (monto + iva)
            if p.get("factura_id") is not None:
                factura_ids_aprobadas.add(p.get("factura_id"))

        elif est == "pendiente":
            c_pendiente += 1
            total_por_cobrar += (monto + iva)

        else:  # anulado u otros
            c_anulado += 1
            total_anulado += (monto + iva)

    return {
        "total_recaudado": round(total_aprobado, 2),
        "total_iva": round(total_iva_aprobado, 2),
        "total_facturas": len(factura_ids_aprobadas),
        "total_pagos": len(pagos_filtrados),

        "detalle_estados": {
            "pagos_aprobados": c_aprobado,
            "pagos_pendientes": c_pendiente,
            "pagos_anulados": c_anulado,
        },
        "otros_ingresos": {
            "total_por_cobrar": round(total_por_cobrar, 2),
            "total_anulado": round(total_anulado, 2),
        },

        "filtros": {"fecha_inicio": fecha_inicio or "", "fecha_fin": fecha_fin or ""}
    }

# ==========================
# REPORTE DE CLIENTES
# ==========================
@router.get("/clientes")
def reporte_clientes():
    reporte = []

    for cliente in clientes_db:
        cliente_id = cliente.get("id")

        reservas_cliente = [r for r in reservas_db if r.get("cliente_id") == cliente_id]
        reserva_ids = {r.get("id") for r in reservas_cliente}

        facturas_cliente = [f for f in facturas_db if f.get("reserva_id") in reserva_ids]
        factura_ids = {f.get("id") for f in facturas_cliente}

        pagos_cliente = [p for p in pagos_db if p.get("factura_id") in factura_ids]

        # total_pagado con IVA 15% si no existe "iva" en el pago
        total_pagado = 0.0
        for p in pagos_cliente:
            monto = float(p.get("monto", 0) or 0)
            iva = p.get("iva")
            if iva is None:
                iva = round(monto * 0.15, 2)
            else:
                iva = float(iva or 0)
            total_pagado += (monto + iva)

        reporte.append({
            "cliente_id": cliente_id,
            "cliente_nombre": cliente.get("nombre"),
            "cliente_identificacion": cliente.get("identificacion"),
            "total_reservas": len(reservas_cliente),
            "total_facturas": len(facturas_cliente),
            "total_pagado": round(total_pagado, 2),
        })

    return reporte


# ==========================
# REPORTE DE HABITACIONES
# ==========================
@router.get("/habitaciones")
def reporte_habitaciones():
    total = len(habitaciones_db)
    disponibles = len([h for h in habitaciones_db if h.get("disponible", False) is True])
    ocupadas = total - disponibles
    porcentaje = (ocupadas / total * 100) if total > 0 else 0

    habitaciones_detalle = []
    for hab in habitaciones_db:
        reservas_activas = [
            r for r in reservas_db
            if r.get("habitacion_id") == hab.get("id")
            and r.get("estado") in ["pendiente", "confirmada"]
        ]

        habitaciones_detalle.append({
            "id": hab.get("id"),
            "numero": hab.get("numero"),
            "tipo": hab.get("tipo"),
            "precio": hab.get("precio"),
            "disponible": hab.get("disponible"),
            "estado": "Ocupada" if reservas_activas else "Disponible",
            "reservas_activas": len(reservas_activas)
        })

    return {
        "total_habitaciones": total,
        "habitaciones_disponibles": disponibles,
        "habitaciones_ocupadas": ocupadas,
        "porcentaje_ocupacion": round(porcentaje, 2),
        "habitaciones": habitaciones_detalle
    }


# ==========================
# REPORTE DE FACTURAS
# ==========================
@router.get("/facturas")
def reporte_facturas(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
):
    facturas_filtradas = facturas_db

    if fecha_inicio:
        facturas_filtradas = [f for f in facturas_filtradas if f.get("fecha", "") >= fecha_inicio]
    if fecha_fin:
        facturas_filtradas = [f for f in facturas_filtradas if f.get("fecha", "") <= fecha_fin]

    emitidas = len([f for f in facturas_filtradas if f.get("estado") == "emitida"])
    pendientes = len([f for f in facturas_filtradas if f.get("estado") == "pendiente"])
    canceladas = len([f for f in facturas_filtradas if f.get("estado") == "cancelada"])
    total_monto = sum(float(f.get("total", 0) or 0) for f in facturas_filtradas)

    facturas_detalle = []
    for factura in facturas_filtradas:
        cliente = next((c for c in clientes_db if c.get("id") == factura.get("cliente_id")), {})

        facturas_detalle.append({
            "factura_id": factura.get("id"),
            "cliente": cliente.get("nombre") if cliente else "N/A",
            "reserva_id": factura.get("reserva_id"),
            "total": factura.get("total"),
            "fecha": factura.get("fecha"),
            "estado": factura.get("estado")
        })

    return {
        "total_facturas": len(facturas_filtradas),
        "total_monto": round(total_monto, 2),
        "facturas_emitidas": emitidas,
        "facturas_pendientes": pendientes,
        "facturas_canceladas": canceladas,
        "facturas": facturas_detalle
    }


# ==========================
# REPORTE DE RESERVAS
# ==========================
@router.get("/reservas")
def reporte_reservas(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None
):
    reservas_filtradas = reservas_db

    if fecha_inicio:
        reservas_filtradas = [r for r in reservas_filtradas if r.get("fecha_inicio", "") >= fecha_inicio]
    if fecha_fin:
        reservas_filtradas = [r for r in reservas_filtradas if r.get("fecha_fin", "") <= fecha_fin]

    confirmadas = len([r for r in reservas_filtradas if r.get("estado") == "confirmada"])
    pendientes = len([r for r in reservas_filtradas if r.get("estado") == "pendiente"])
    canceladas = len([r for r in reservas_filtradas if r.get("estado") == "cancelada"])

    reservas_detalle = []
    for reserva in reservas_filtradas:
        cliente = next((c for c in clientes_db if c.get("id") == reserva.get("cliente_id")), {})
        habitacion = next((h for h in habitaciones_db if h.get("id") == reserva.get("habitacion_id")), {})

        reservas_detalle.append({
            "reserva_id": reserva.get("id"),
            "cliente": cliente.get("nombre") if cliente else "N/A",
            "habitacion": habitacion.get("numero") if habitacion else "N/A",
            "fecha_inicio": reserva.get("fecha_inicio"),
            "fecha_fin": reserva.get("fecha_fin"),
            "estado": reserva.get("estado")
        })

    return {
        "total_reservas": len(reservas_filtradas),
        "reservas_confirmadas": confirmadas,
        "reservas_pendientes": pendientes,
        "reservas_canceladas": canceladas,
        "reservas": reservas_detalle
    }


# ==========================
# REPORTE GENERAL
# ==========================
@router.get("/general")
def reporte_general():
    total_recaudado = 0.0
    for p in pagos_db:
        if (p.get("estado") or "").lower() != "aprobado":
            continue
        monto = float(p.get("monto", 0) or 0)
        iva = p.get("iva")
        iva = round(monto * 0.15, 2) if iva is None else float(iva or 0)
        total_recaudado += (monto + iva)

    return {
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resumen": {
            "total_clientes": len(clientes_db),
            "total_habitaciones": len(habitaciones_db),
            "total_reservas": len(reservas_db),
            "total_facturas": len(facturas_db),
            "total_pagos": len(pagos_db)
        },
        "ingresos": {
            "total_recaudado": round(total_recaudado, 2)
        }
    }


# ==========================
# LIMPIAR TODOS LOS DATOS
# ==========================
@router.delete("/limpiar-todo")
def limpiar_todo():
    stats = {
        "clientes_eliminados": len(clientes_db),
        "habitaciones_eliminadas": len(habitaciones_db),
        "reservas_eliminadas": len(reservas_db),
        "facturas_eliminadas": len(facturas_db),
        "pagos_eliminados": len(pagos_db),
    }

    clientes_db.clear()
    habitaciones_db.clear()
    reservas_db.clear()
    facturas_db.clear()
    pagos_db.clear()

    return {
        "ok": True,
        "message": "⚠️ Todos los datos han sido eliminados",
        "estadisticas": stats
    }