import pytest

from app.database.models import Author
from app.services.author_service import AuthorService


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

    service = AuthorService(db_session)

    authors = service.get_all_authors()

    assert len(authors) == 2
    assert authors[0].last_name == "Orwell"
    assert authors[1].last_name == "Tolkien"


def test_get_author_by_id(db_session):
    author = create_author(
        db_session,
        "J.R.R.",
        "Tolkien",
    )

    service = AuthorService(db_session)

    retrieved_author = service.get_author_by_id(author.id)

    assert retrieved_author is not None
    assert retrieved_author.first_name == "J.R.R."
    assert retrieved_author.last_name == "Tolkien"

def test_create_author(db_session):
    service = AuthorService(db_session)

    author = service.create_author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )

    assert author.id is not None
    assert author.first_name == "J.R.R."
    assert author.last_name == "Tolkien"

def test_create_author_rejects_blank_first_name(db_session):
    service = AuthorService(db_session)

    with pytest.raises(ValueError, match="First name cannot be blank"):
        service.create_author(
            first_name="",
            last_name="Tolkien",
        )

def test_create_author_rejects_blank_last_name(db_session):
    service = AuthorService(db_session)

    with pytest.raises(ValueError, match="Last name cannot be blank"):
        service.create_author(
            first_name="J.R.R.",
            last_name="",
        )

def test_create_author_strips_whitespace(db_session):
    service = AuthorService(db_session)

    author = service.create_author(
        first_name="  J.R.R.  ",
        last_name="  Tolkien  ",
    )

    assert author.first_name == "J.R.R."
    assert author.last_name == "Tolkien"