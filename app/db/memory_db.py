# app/db/memory_db.py

from typing import List, Dict

# app/db/memory_db.py
clientes_db: list[dict] = []
habitaciones_db: list[dict] = []
reservas_db: list[dict] = []
facturas_db: list[dict] = []
pagos_db: list[dict] = []

def next_id(db_list: List[Dict]) -> int:
    return max([x.get("id", 0) for x in db_list], default=0) + 1

def find_by_id(db_list: List[Dict], _id: int):
    return next((x for x in db_list if x.get("id") == _id), None)