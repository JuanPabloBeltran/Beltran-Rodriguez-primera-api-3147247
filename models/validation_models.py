from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class User(BaseModel):
    id: int = Field(..., gt=0, description="ID del usuario (mayor a 0)")
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18, le=100, description="Edad entre 18 y 100")

class Product(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0, description="Precio mayor a 0")
    in_stock: bool = True

class Order(BaseModel):
    order_id: int = Field(..., gt=0)
    products: List[Product]
    total: float = Field(..., gt=0)

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
