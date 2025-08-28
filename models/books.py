from pydantic import BaseModel, Field, validator
from enum import Enum

class BookStatus(str, Enum):
    available = "available"
    checked_out = "checked_out"
    reserved = "reserved"

class BookGenre(str, Enum):
    fiction = "fiction"
    nonfiction = "nonfiction"
    science = "science"
    fantasy = "fantasy"

class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    author: str
    year: int = Field(..., ge=0, le=2025)
    genre: BookGenre
    isbn: str
    status: BookStatus = BookStatus.available

    @validator("isbn")
    def validate_isbn(cls, v):
        if not (len(v) == 10 or len(v) == 13):
            raise ValueError("El ISBN debe tener 10 o 13 caracteres")
        if not v.isdigit():
            raise ValueError("El ISBN debe contener solo números")
        return v

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "year": 1967,
                "genre": "fiction",
                "isbn": "9780307474728",
                "status": "available"
            }
        }
