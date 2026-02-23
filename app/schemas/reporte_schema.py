from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReporteIngresos(BaseModel):
    total_recaudado: float
    total_facturas: int
    total_pagos: int
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None

class ReporteCliente(BaseModel):
    cliente_id: int
    cliente_nombre: str
    cliente_identificacion: str
    total_reservas: int
    total_facturas: int
    total_pagado: float
    reservas: List[dict]

class ReporteHabitaciones(BaseModel):
    total_habitaciones: int
    habitaciones_disponibles: int
    habitaciones_ocupadas: int
    porcentaje_ocupacion: float
    habitaciones: List[dict]

class ReporteFacturas(BaseModel):
    total_facturas: int
    total_monto: float
    facturas_emitidas: int
    facturas_pendientes: int
    facturas_canceladas: int
    facturas: List[dict]

class ReporteReservas(BaseModel):
    total_reservas: int
    reservas_confirmadas: int
    reservas_pendientes: int
    reservas_canceladas: int
    reservas: List[dict]