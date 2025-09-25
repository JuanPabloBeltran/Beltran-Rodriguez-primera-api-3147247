# Dashboard genérico de métricas
from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
def dashboard():
    # Datos de ejemplo para flores
    flores = [
        {"id": 1, "nombre": "Flor Roja"},
        {"id": 2, "nombre": "Flor Azul"},
        {"id": 3, "nombre": "Flor Amarilla"}
    ]
    inventario = []
    for flor in flores:
        inv = get_inventario(flor["id"])
        precio = get_precio(flor["id"])
        inventario.append({
            "nombre": flor["nombre"],
            "stock": inv["stock"] if inv else "No disponible",
            "ubicacion": inv["ubicacion"] if inv else "No disponible",
            "precio": precio if precio else "No disponible"
        })
    return {
        "dashboard": "Floristería Jardín Natural - Inventario en tiempo real",
        "productos": inventario,
        "mensaje": "Catálogo optimizado para BELTRAN RODRIGUEZ (Tipo D)"
    }
