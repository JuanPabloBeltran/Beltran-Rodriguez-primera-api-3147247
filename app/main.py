# app/main.py
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Header, Depends, status
from pydantic import BaseModel

app = FastAPI(title="API Plomería - plumber_")

# --- Schemas
class ReparacionBase(BaseModel):
    cliente: str
    direccion: str
    tipo_problema: str
    estado: str
    costo_estimado: float

class Reparacion(ReparacionBase):
    id: int

# --- Simular DB en memoria
_reparaciones: Dict[int, Dict] = {}
_next_id = 1

# --- Autenticación simple (X-API-KEY)
def get_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != "secret-plumber-key":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")
    return x_api_key

# --- Endpoints CRUD
@app.post("/plumber/reparaciones/", response_model=Reparacion, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_api_key)])
def create_reparacion(reparacion: ReparacionBase):
    global _next_id
    item = reparacion.model_dump()   # <--- antes: reparacion.dict()
    item_id = _next_id
    item["id"] = item_id
    _reparaciones[item_id] = item
    _next_id += 1
    return item

@app.get("/plumber/reparaciones/", response_model=List[Reparacion])
def list_reparaciones():
    return list(_reparaciones.values())

@app.get("/plumber/reparaciones/{reparacion_id}", response_model=Reparacion)
def get_reparacion(reparacion_id: int):
    item = _reparaciones.get(reparacion_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return item

@app.put("/plumber/reparaciones/{reparacion_id}", response_model=Reparacion, dependencies=[Depends(get_api_key)])
def update_reparacion(reparacion_id: int, reparacion: ReparacionBase):
    if reparacion_id not in _reparaciones:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    item = reparacion.model_dump()   # <--- antes: reparacion.dict()
    item["id"] = reparacion_id
    _reparaciones[reparacion_id] = item
    return item

@app.delete("/plumber/reparaciones/{reparacion_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_api_key)])
def delete_reparacion(reparacion_id: int):
    if reparacion_id not in _reparaciones:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    del _reparaciones[reparacion_id]
    return None
