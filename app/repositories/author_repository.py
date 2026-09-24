from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Author

class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Author]:
        statement = (
            select(Author)
            .order_by(Author.last_name, Author.first_name)
        )

        return list(self.db.scalars(statement).all())

    def get_by_id(self, author_id: int) -> Author | None:
        return self.db.get(Author, author_id)

    def create(self, author: Author) -> Author:
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)

        return author