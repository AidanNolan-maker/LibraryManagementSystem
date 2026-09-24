from sqlalchemy.orm import Session

from app.database.models import Author
from app.repositories.author_repository import AuthorRepository

class AuthorService:
    def __init__(self, db: Session):
        self.repository = AuthorRepository(db)

    def get_all_authors(self) -> list[Author]:
        return self.repository.get_all()

    def get_author_by_id(self, author_id: int) -> Author | None:
        return self.repository.get_by_id(author_id)

    def create_author(
            self,
            first_name: str,
            last_name: str,
    ) -> Author:
        first_name = first_name.strip()
        last_name = last_name.strip()

        if not first_name:
            raise ValueError("First name cannot be blank")

        if not last_name:
            raise ValueError("Last name cannot be blank")

        author = Author(
            first_name=first_name,
            last_name=last_name,
        )

        return self.repository.create(author)