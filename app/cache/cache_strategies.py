# Estrategias universales de caching para inventario y precios (Tipo D)
from .redis_config import redis_client
import json

def cache_inventario(elemento_id, inventario):
    key = f"inventario:{elemento_id}"
    redis_client.set(key, json.dumps(inventario))

def get_inventario(elemento_id):
    key = f"inventario:{elemento_id}"
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def cache_precio(elemento_id, precio):
    key = f"precio:{elemento_id}"
    redis_client.set(key, precio)

def get_precio(elemento_id):
    key = f"precio:{elemento_id}"
    value = redis_client.get(key)
    if value:
        return float(value)
    return None
