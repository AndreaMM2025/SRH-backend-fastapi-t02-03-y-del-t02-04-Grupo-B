from fastapi import APIRouter
from app.schemas.reporte_schema import ReporteIngresos
from app.routers.facturas import facturas_db
from app.routers.pagos import pagos_db

router = APIRouter(
    prefix="/api/reportes",
    tags=["Reportes"]
)

@router.get("/ingresos", response_model=ReporteIngresos)
def reporte_ingresos():
    total = sum(pago["monto"] for pago in pagos_db)
    return {"total_recaudado": total}
