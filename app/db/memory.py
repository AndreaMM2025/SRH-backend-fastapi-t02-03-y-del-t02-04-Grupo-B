# app/db/memory.py
from typing import List, Dict

clientes_db: List[Dict] = []
habitaciones_db: List[Dict] = []
reservas_db: List[Dict] = []
facturas_db: List[Dict] = []


def next_id(db_list: List[Dict]) -> int:
    return max([x.get("id", 0) for x in db_list], default=0) + 1