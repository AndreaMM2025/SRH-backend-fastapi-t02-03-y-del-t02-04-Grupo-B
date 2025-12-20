from fastapi import FastAPI
from app.routers import clientes

app = FastAPI(title="SRH Backend")

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}

app.include_router(clientes.router)
