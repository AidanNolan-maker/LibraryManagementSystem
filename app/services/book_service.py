from sqlalchemy.orm import Session

from app.database.models import Book
from app.repositories.book_repository import BookRepository
from app.repositories.book_copy_repository import BookCopyRepository
from app.repositories.loan_repository import LoanRepository

class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)
        self.book_copy_repository = BookCopyRepository(db)
        self.loan_repository = LoanRepository(db)

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
            title = title.strip()
            isbn = isbn.strip()
            
            if not title:
                raise ValueError("Title cannot be blank")

            if not isbn:
                raise ValueError("ISBN cannot be blank")

            if self.repository.get_by_isbn(isbn) is not None:
                raise ValueError("A book with this ISBN already exists")
            
            book = Book(
                title=title,
                isbn=isbn,
                publication_year=publication_year,
                genre=genre,
                author_id=author_id,
            )

            return self.repository.create(book)

    def update_book(self, book: Book) -> Book:
        book.title = book.title.strip()
        book.isbn = book.isbn.strip()

        if not book.title:
            raise ValueError("Title cannot be blank")

        if not book.isbn:
            raise ValueError("ISBN cannot be blank")

        with self.repository.db.no_autoflush:
            existing_book = self.repository.get_by_isbn(book.isbn)

        if existing_book is not None and existing_book.id != book.id:
            raise ValueError("A book with this ISBN already exists")

        return self.repository.update(book)

    def archive_book(self, book: Book) -> None:
        copies = self.book_copy_repository.get_by_book_id(book.id)

        for copy in copies:
            active_loan = self.loan_repository.get_active_by_copy_id(copy.id)

            if active_loan is not None:
                raise ValueError(
                    "Cannot archive a book while one or more copies are currently loaned out"
                )

        book.is_archived = True
        self.repository.update(book)