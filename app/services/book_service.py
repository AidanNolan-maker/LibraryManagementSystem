from sqlalchemy.orm import Session

from app.database.models import Book
from app.repositories.book_repository import BookRepository

class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    def get_all_books(self) -> list[Book]:
        return self.repository.get_all()

    def get_book_by_id(self, book_id: int) -> Book | None:
        return self.repository.get_by_id(book_id)

    def get_book_by_isbn(self, isbn: str) -> Book | None:
        return self.repository.get_by_isbn(isbn)

    def search_books(self, search_term: str) -> list[Book]:
        return self.repository.search(search_term)

    def create_book(
            self,
            title: str,
            isbn: str,
            publication_year: int | None,
            genre: str | None,
            author_id: int, 
        ) -> Book:
            book = Book(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                genre=genre,
                author_id=author_id,
            )

            return self.repository.create(book)

    def update_book(self, book: Book) -> Book:
        return self.repository.update(book)

    def delete_book(self, book: Book) -> None:
        self.repository.delete(book)