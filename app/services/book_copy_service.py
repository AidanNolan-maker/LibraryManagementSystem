from sqlalchemy.orm import Session

from app.database.models import BookCopy
from app.repositories.book_copy_repository import BookCopyRepository

class BookCopyService:
    def __init__(self, db: Session):
        self.repository = BookCopyRepository(db)

    def get_all_copies(self) -> list[BookCopy]:
        return self.repository.get_all()

    def get_copy_by_id(self, copy_id: int) -> BookCopy | None:
        return self.repository.get_by_id(copy_id)

    def get_copies_for_book(self, book_id: int) -> list[BookCopy]:
        return self.repository.get_by_book_id(book_id)

    def create_copy(self, book_id: int) -> BookCopy:
        book_copy = BookCopy(
            book_id=book_id,
            status="AVAILABLE",
        )
        return self.repository.create(book_copy)

    def update_copy(self, book_copy: BookCopy) -> BookCopy:
        if book_copy.status not in {"AVAILABLE", "LOANED"}:
            raise ValueError("Invalid book copy status")

        return self.repository.update(book_copy)

    def delete_copy(self, book_copy: BookCopy) -> None:
        self.repository.delete(book_copy)