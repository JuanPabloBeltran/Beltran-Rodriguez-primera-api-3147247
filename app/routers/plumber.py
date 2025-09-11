from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Modelo de datos
class ReparacionPlomeria(BaseModel):
    cliente: str
    direccion: str
    tipo_problema: str
    estado: str
    costo_estimado: float

# Endpoint para crear reparaciones
@router.post("/reparaciones/", status_code=201)
def create_reparacion(reparacion: ReparacionPlomeria):
    return {"mensaje": "Reparación creada con éxito", "data": reparacion}
