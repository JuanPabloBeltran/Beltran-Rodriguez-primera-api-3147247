# routers/categorias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import crear_categoria, obtener_categorias, obtener_categoria_con_productos
from schemas import Categoria, CategoriaCreate
from typing import List

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("/", response_model=Categoria)
def crear_categoria_endpoint(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crear_categoria(db, categoria)

@router.get("/", response_model=List[Categoria])
def listar_categorias(db: Session = Depends(get_db)):
    return obtener_categorias(db)

@router.get("/{categoria_id}", response_model=Categoria)
def obtener_categoria_endpoint(categoria_id: int, db: Session = Depends(get_db)):
    cat = obtener_categoria_con_productos(db, categoria_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return cat
