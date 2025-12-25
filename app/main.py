from fastapi import FastAPI
from app.routers import clientes, habitaciones, reservas, facturas, pagos, reportes

app = FastAPI(title="Sistema de Reservas de Hoteles (SRH) - Backend")

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

app.include_router(clientes.router)
app.include_router(habitaciones.router)
app.include_router(reservas.router)
app.include_router(facturas.router)
app.include_router(pagos.router)
app.include_router(reportes.router)

"""
Documentación del backend SRH:
Swagger UI: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json
"""
