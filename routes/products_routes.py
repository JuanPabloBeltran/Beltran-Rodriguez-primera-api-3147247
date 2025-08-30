from fastapi import APIRouter, HTTPException
from typing import List
from models.products import Product, ProductResponse
from data.products_data import products_db

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products():
    return products_db

@router.post("/", response_model=ProductResponse)
def create_product(product: Product):
    products_db.append(product)
    return {"message": "Producto creado con éxito", "product": product}

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Producto no encontrado")
