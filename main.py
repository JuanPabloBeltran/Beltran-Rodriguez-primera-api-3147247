from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Union
from enum import Enum
from datetime import datetime
import asyncio
import os, sys

app = FastAPI(
    title="Mi Biblioteca + API FastAPI",
    description="API combinada: Biblioteca Personal + Productos + Usuarios",
    version="1.0.0"
)

# ------------------------------
# MODELOS Pydantic
# ------------------------------
class BookStatus(str, Enum):
    to_read = "to_read"
    reading = "reading"
    finished = "finished"
    paused = "paused"

class BookGenre(str, Enum):
    fiction = "fiction"
    non_fiction = "non_fiction"
    science = "science"
    biography = "biography"
    history = "history"
    technology = "technology"
    other = "other"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    genre: BookGenre = Field(default=BookGenre.other)
    pages: Optional[int] = Field(None, ge=1, le=10000)
    publication_year: Optional[int] = Field(None, ge=1000, le=datetime.now().year)
    status: BookStatus = Field(default=BookStatus.to_read)
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)

    @validator('isbn')
    def validate_isbn(cls, v):
        if v:
            clean = v.replace('-', '').replace(' ', '')
            if len(clean) not in [10, 13] or not clean.isdigit():
                raise ValueError('ISBN debe tener 10 o 13 dígitos y solo números')
        return v

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    genre: Optional[BookGenre]
    pages: Optional[int]
    publication_year: Optional[int]
    status: Optional[BookStatus]
    rating: Optional[int]
    notes: Optional[str]

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[Dict[str, Union[str, int, bool]]]
    total: int
    message: str = "List retrieved"

class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None
    active: bool = True

# ------------------------------
# BASES DE DATOS EN MEMORIA
# ------------------------------
books_db: List[Dict] = []
products: List[Dict[str, Union[str, int, bool]]] = []

# ------------------------------
# FUNCIONES ASYNC DE APOYO
# ------------------------------
async def validate_isbn_external(isbn: str) -> bool:
    await asyncio.sleep(0.5)
    clean = isbn.replace('-', '').replace(' ', '')
    return len(clean) in [10, 13]

async def backup_book_data(book_data: dict) -> dict:
    await asyncio.sleep(0.3)
    return {"backup_id": f"bk_{datetime.now().timestamp()}", "status": "success"}

async def get_book_metadata(title: str, author: str) -> dict:
    await asyncio.sleep(0.4)
    return {"goodreads_rating": 4.2, "amazon_price": 15.99, "availability": "in_stock"}

# ------------------------------
# ENDPOINTS BÁSICOS
# ------------------------------
@app.get("/")
def home() -> Dict[str, str]:
    return {"message": "Mi Biblioteca + API FastAPI"}

@app.get("/info/setup")
def info_setup() -> Dict[str, str]:
    return {
        "python_version": sys.version,
        "python_path": sys.executable,
        "working_directory": os.getcwd(),
        "virtual_env": os.environ.get("VIRTUAL_ENV", "No detectado"),
        "user": os.environ.get("USER", os.environ.get("USERNAME", "No detectado")),
        "hostname": os.environ.get("HOSTNAME", "No detectado")
    }

@app.get("/my-profile")
def my_profile() -> Dict[str, Union[str, bool, int]]:
    return {
        "name": "Sebastian Manrique",
        "bootcamp": "FastAPI",
        "week": 2,
        "date": "2025",
        "likes_fastapi": True
    }

# ------------------------------
# CRUD LIBROS
# ------------------------------
@app.post("/books", response_model=BookResponse)
async def create_book(book: BookCreate):
    if book.isbn:
        valid = await validate_isbn_external(book.isbn)
        if not valid:
            raise HTTPException(status_code=400, detail="ISBN inválido")
    now = datetime.now()
    book_dict = book.dict()
    book_dict.update({"id": len(books_db)+1, "created_at": now, "updated_at": now})
    books_db.append(book_dict)
    asyncio.create_task(backup_book_data(book_dict))
    return book_dict

@app.get("/books", response_model=List[BookResponse])
def list_books():
    return books_db

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    for b in books_db:
        if b["id"] == book_id:
            return b
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated: BookCreate):
    for idx, b in enumerate(books_db):
        if b["id"] == book_id:
            updated_dict = updated.dict()
            updated_dict.update({"id": book_id, "created_at": b["created_at"], "updated_at": datetime.now()})
            books_db[idx] = updated_dict
            return updated_dict
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.patch("/books/{book_id}", response_model=BookResponse)
def patch_book(book_id: int, updated: BookUpdate):
    for idx, b in enumerate(books_db):
        if b["id"] == book_id:
            for k, v in updated.dict(exclude_unset=True).items():
                b[k] = v
            b["updated_at"] = datetime.now()
            books_db[idx] = b
            return b
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for idx, b in enumerate(books_db):
        if b["id"] == book_id:
            removed = books_db.pop(idx)
            return {"message": "Libro eliminado", "book": removed}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# ------------------------------
# ENDPOINTS BÚSQUEDA
# ------------------------------
@app.get("/books/search/title", response_model=List[BookResponse])
def search_books_title(title: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    results = [b for b in books_db if title.lower() in b["title"].lower()]
    return results[:limit]

@app.get("/books/search/author", response_model=List[BookResponse])
def search_books_author(author: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)):
    results = [b for b in books_db if author.lower() in b["author"].lower()]
    return results[:limit]

# ------------------------------
# ENDPOINT ASYNC METADATA
# ------------------------------
@app.get("/books/{book_id}/metadata")
async def book_metadata(book_id: int):
    for b in books_db:
        if b["id"] == book_id:
            meta = await get_book_metadata(b["title"], b["author"])
            return {"book": b, "metadata": meta}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# ------------------------------
# CRUD PRODUCTOS
# ------------------------------
@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return ProductResponse(**product_dict, message="Product created successfully")

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(products=products, total=len(products))

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductResponse:
    for product in products:
        if product["id"] == product_id:
            return ProductResponse(**product, message="Product found successfully")
    raise HTTPException(status_code=404, detail="Product not found")

# ------------------------------
# CRUD USUARIOS
# ------------------------------
@app.post("/users")
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}

# ------------------------------
# SERVIDOR
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
