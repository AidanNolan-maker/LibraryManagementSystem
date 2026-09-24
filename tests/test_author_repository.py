from app.database.models import Author
from app.repositories.author_repository import AuthorRepository


def create_author(db_session, first_name, last_name):
    author = Author(
        first_name=first_name,
        last_name=last_name,
    )

    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    return author


def test_get_all_authors(db_session):
    create_author(db_session, "J.R.R.", "Tolkien")
    create_author(db_session, "George", "Orwell")

    repository = AuthorRepository(db_session)

    authors = repository.get_all()

    assert len(authors) == 2
    assert authors[0].last_name == "Orwell"
    assert authors[1].last_name == "Tolkien"


def test_get_author_by_id(db_session):
    author = create_author(
        db_session,
        "J.R.R.",
        "Tolkien",
    )

    repository = AuthorRepository(db_session)

    retrieved_author = repository.get_by_id(author.id)

    assert retrieved_author is not None
    assert retrieved_author.first_name == "J.R.R."
    assert retrieved_author.last_name == "Tolkien"

def test_create_author(db_session):
    repository = AuthorRepository(db_session)

    author = Author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )

    created_author = repository.create(author)

    assert created_author.id is not None
    assert created_author.first_name == "J.R.R."
    assert created_author.last_name == "Tolkien"