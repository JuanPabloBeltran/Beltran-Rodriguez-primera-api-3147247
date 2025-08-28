from models.books import Book, BookGenre

books_db = [
    Book(id=1, title="Cien Años de Soledad", author="Gabriel García Márquez",
        year=1967, genre=BookGenre.fiction, isbn="1234567890"),
    Book(id=2, title="El Quijote", author="Miguel de Cervantes",
        year=1605, genre=BookGenre.fiction, isbn="0987654321"),
]
