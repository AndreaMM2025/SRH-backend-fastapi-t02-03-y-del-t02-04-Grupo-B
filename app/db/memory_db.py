from typing import List, Dict, Any

# ======= DBs en memoria =======
clientes_db: List[Dict[str, Any]] = []
habitaciones_db: List[Dict[str, Any]] = [] 
reservas_db: List[Dict[str, Any]] = []
facturas_db: List[Dict[str, Any]] = []
pagos_db: List[Dict[str, Any]] = []
usuarios_db: List[Dict[str, Any]] = []

def next_id(db: List[Dict[str, Any]]) -> int:
    return max([x.get("id", 0) for x in db], default=0) + 1

def find_by_id(db: List[Dict[str, Any]], _id: int):
    return next((x for x in db if x.get("id") == _id), None)


def delete_by_id(db: List[Dict[str, Any]], _id: int) -> bool:
    idx = next((i for i, x in enumerate(db) if x.get("id") == _id), None)
    if idx is None:
        return False
    db.pop(idx)
    return True