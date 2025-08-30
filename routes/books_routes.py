from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.books import Book
from data.books_data import books_db

router = APIRouter()

@router.get("/", response_model=List[Book])
def get_books(limit: Optional[int] = Query(None, ge=1, le=50)):
    return books_db[:limit] if limit else books_db

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.post("/", response_model=Book)
def create_book(book: Book):
    books_db.append(book)
    return book

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for idx, book in enumerate(books_db):
        if book.id == book_id:
            books_db[idx] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.delete("/{book_id}")
def delete_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            books_db.remove(book)
            return {"message": "Libro eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")
