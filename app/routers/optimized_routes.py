# Endpoints optimizados para catálogo de elementos (Tipo D)

from fastapi import APIRouter, HTTPException
from app.models.optimized_models import ElementoCatalogo, InventarioElemento
from app.cache.cache_strategies import get_inventario, get_precio, cache_inventario, cache_precio


router = APIRouter()

# Endpoint para cargar datos de ejemplo en Redis
@router.post("/catalogo/cargar-ejemplo")
def cargar_ejemplo():
    # Ejemplo de productos
    productos = [
        {"id": 1, "nombre": "Flor Roja", "precio": 12.5, "stock": 100, "ubicacion": "A1"},
        {"id": 2, "nombre": "Flor Azul", "precio": 15.0, "stock": 80, "ubicacion": "A2"},
        {"id": 3, "nombre": "Flor Amarilla", "precio": 10.0, "stock": 120, "ubicacion": "B1"}
    ]
    for prod in productos:
        cache_inventario(prod["id"], {"stock": prod["stock"], "ubicacion": prod["ubicacion"]})
        cache_precio(prod["id"], prod["precio"])
    return {"msg": "Datos de ejemplo cargados en Redis", "productos": productos}

# Ejemplo: obtener inventario y precio de un elemento
@router.get("/elemento/{elemento_id}")
def get_elemento(elemento_id: int):
    inventario = get_inventario(elemento_id)
    precio = get_precio(elemento_id)
    if inventario is None or precio is None:
        raise HTTPException(status_code=404, detail="Elemento no encontrado en cache")
    return {"elemento_id": elemento_id, "inventario": inventario, "precio": precio}

# Ejemplo: búsqueda optimizada de catálogo
@router.get("/catalogo/buscar")
def buscar_catalogo(nombre: str):
    # Aquí iría la consulta optimizada a la base de datos (simulada)
    return {"resultados": [f"Elemento encontrado: {nombre}"]}
