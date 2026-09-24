from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import BookCopy

class BookCopyRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[BookCopy]:
        statement = select(BookCopy).order_by(BookCopy.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, copy_id: int) -> BookCopy | None:
        return self.db.get(BookCopy, copy_id)

    def get_by_book_id(self, book_id: int) -> list[BookCopy]:
        statement = (
            select(BookCopy)
            .where(BookCopy.book_id == book_id)
            .order_by(BookCopy.id)
        )
        return list(self.db.scalars(statement).all())

    def create(self, book_copy: BookCopy) -> BookCopy:
        self.db.add(book_copy)
        self.db.commit()
        self.db.refresh(book_copy)
        return book_copy

    def update(self, book_copy: BookCopy) -> BookCopy:
        self.db.commit()
        self.db.refresh(book_copy)
        return book_copy

    def delete(self, book_copy: BookCopy) -> None:
        self.db.delete(book_copy)
        self.db.commit()