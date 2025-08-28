from pydantic import BaseModel, Field

class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)

class ProductResponse(BaseModel):
    message: str
    product: Product
