from sqlalchemy import select, case, func
from sqlalchemy.orm import Session

from app.database.models import Book, BookCopy

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
        search_pattern = f"%{search_term}%"

        statement = (
            select(Book)
            .where(
                Book.is_archived.is_(False),
                (
                    Book.title.ilike(search_pattern)
                    | Book.isbn.ilike(search_pattern)
                ),
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

    def get_copy_counts_for_books(self) -> dict[int, dict[str, int]]:
        statement = (
            select(
                Book.id,
                func.count(BookCopy.id).label("total"),
                func.sum(
                    case(
                        (BookCopy.status == "AVAILABLE", 1),
                        else_=0,
                    )
                ).label("available"),
                func.sum(
                    case(
                        (BookCopy.status == "LOANED", 1),
                        else_=0,
                    )
                ).label("loaned"),
            )
            .outerjoin(BookCopy, BookCopy.book_id == Book.id)
            .where(Book.is_archived.is_(False))
            .group_by(Book.id)
        )

        results = self.db.execute(statement).all()

        return {
            book_id: {
                "total": total,
                "available": available,
                "loaned": loaned,
            }
            for book_id, total, available, loaned in results
        }