from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Book

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Book]:
        statement = (
            select(Book)
            .where(Book.is_archived.is_(False))
            .order_by(Book.title)
        )

        return list(self.db.scalars(statement).all())

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_isbn(self, isbn: str) -> Book | None:
        statement = select(Book).where(Book.isbn == isbn)

        return self.db.scalars(statement).first()

    def search(self, search_term: str) -> list[Book]:
        statement = (
            select(Book)
            .where(
                Book.is_archived.is_(False),
                Book.title.ilike(f"%{search_term}%"),
            )
            .order_by(Book.title)
        )

        return list(self.db.scalars(statement).all())

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return book

    def update(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)

        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()