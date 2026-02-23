from fastapi import APIRouter, HTTPException, Query
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

# ==========================
# REPORTE DE INGRESOS
# ==========================
@router.get("/habitaciones")
def reporte_habitaciones():
    # ✅ Leer directamente de habitaciones_db
    total = len(habitaciones_db)
    disponibles = len([h for h in habitaciones_db if h.get("disponible", False) == True])
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
        total_pagado = sum(p.get("monto", 0) + p.get("iva", 0) for p in pagos_cliente)
        
        reservas_detalle = []
        for reserva in reservas_cliente:
            habitacion = next((h for h in habitaciones_db if h.get("id") == reserva.get("habitacion_id")), {})
            reservas_detalle.append({
                "reserva_id": reserva.get("id"),
                "fecha_inicio": reserva.get("fecha_inicio"),
                "fecha_fin": reserva.get("fecha_fin"),
                "estado": reserva.get("estado"),
                "habitacion_numero": habitacion.get("numero"),
                "habitacion_tipo": habitacion.get("tipo")
            })
        
        reporte.append({
            "cliente_id": cliente_id,
            "cliente_nombre": cliente.get("nombre"),
            "cliente_identificacion": cliente.get("identificacion"),
            "total_reservas": len(reservas_cliente),
            "total_facturas": len(facturas_cliente),
            "total_pagado": round(total_pagado, 2),
            "reservas": reservas_detalle
        })
    
    return reporte

# ==========================
# REPORTE DE HABITACIONES 
# ==========================
@router.get("/habitaciones")
def reporte_habitaciones():
    total = len(habitaciones_db)
    disponibles = len([h for h in habitaciones_db if h.get("disponible", False)])
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
    total_monto = sum(f.get("total", 0) for f in facturas_filtradas)
    
    facturas_detalle = []
    for factura in facturas_filtradas:
        cliente = next((c for c in clientes_db if c.get("id") == factura.get("cliente_id")), {})
        reserva = next((r for r in reservas_db if r.get("id") == factura.get("reserva_id")), {})
        
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
            "total_recaudado": round(sum(p.get("monto", 0) + p.get("iva", 0) for p in pagos_db), 2)
        }
    }

# ==========================
# LIMPIAR TODOS LOS DATOS 
# ==========================
@router.delete("/limpiar-todo")
def limpiar_todo():
    """⚠️ ELIMINA TODOS LOS DATOS DEL SISTEMA"""
    
    stats = {
        "clientes_eliminados": len(clientes_db),
        "habitaciones_eliminadas": len(habitaciones_db),
        "reservas_eliminadas": len(reservas_db),
        "facturas_eliminadas": len(facturas_db),
        "pagos_eliminados": len(pagos_db)
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