from fastapi import APIRouter, HTTPException
from app.db.memory_db import (
    clientes_db, 
    reservas_db, 
    facturas_db, 
    pagos_db,  # ✅ Agregar pagos_db
    next_id, 
    find_by_id
)

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.get("/")
def listar_clientes():
    return clientes_db

@router.post("/")
def crear_cliente(data: dict):
    nuevo = {
        "id": next_id(clientes_db),
        **data
    }
    clientes_db.append(nuevo)
    return nuevo

@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, data: dict):
    c = find_by_id(clientes_db, cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    c.update(data)
    return c

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    c = find_by_id(clientes_db, cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # ✅ 1. ELIMINAR PAGOS (asociados a facturas de este cliente)
    # Obtener todas las facturas del cliente
    facturas_cliente = [f for f in facturas_db if f.get("cliente_id") == cliente_id]
    factura_ids = {f.get("id") for f in facturas_cliente}
    
    # Eliminar pagos de esas facturas
    pagos_db[:] = [p for p in pagos_db if p.get("factura_id") not in factura_ids]
    
    # ✅ 2. ELIMINAR FACTURAS (asociadas a reservas de este cliente)
    # Obtener todas las reservas del cliente
    reservas_cliente = [r for r in reservas_db if r.get("cliente_id") == cliente_id]
    reserva_ids = {r.get("id") for r in reservas_cliente}
    
    # Eliminar facturas de esas reservas
    facturas_db[:] = [f for f in facturas_db if f.get("reserva_id") not in reserva_ids]
    
    # ✅ 3. ELIMINAR RESERVAS del cliente
    reservas_db[:] = [r for r in reservas_db if r.get("cliente_id") != cliente_id]
    
    # ✅ 4. ELIMINAR CLIENTE
    clientes_db[:] = [x for x in clientes_db if x.get("id") != cliente_id]
    
    return {
        "ok": True, 
        "message": "Cliente y todos sus registros asociados eliminados",
        "detalles": {
            "pagos_eliminados": len(factura_ids),
            "facturas_eliminadas": len(factura_ids),
            "reservas_eliminadas": len(reserva_ids)
        }
    }