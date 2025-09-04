from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models.productos as models
import schemas.productos_schemas as schemas
from database import get_db
import crud

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=schemas.Producto)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.crear_producto(db, producto)

@router.get("/", response_model=List[schemas.Producto])
def list_productos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.obtener_productos(db, skip=skip, limit=limit)

@router.get("/{producto_id}", response_model=schemas.Producto)
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = crud.obtener_producto(db, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@router.put("/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto_update: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    prod = crud.actualizar_producto(db, producto_id, producto_update)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return prod

@router.delete("/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = crud.eliminar_producto(db, producto_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
