import pytest

from app.database.models import Author
from app.services.book_service import BookService


def create_author(db_session):
    author = Author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )

    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    return author


def test_create_book(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    assert book.id is not None
    assert book.title == "The Hobbit"
    assert book.isbn == "9780547928227"


def test_get_all_books(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    service.create_book(
        title="The Lord of the Rings",
        isbn="9780618640157",
        publication_year=1954,
        genre="Fantasy",
        author_id=author.id,
    )

    books = service.get_all_books()

    assert len(books) == 2
    assert books[0].title == "The Hobbit"
    assert books[1].title == "The Lord of the Rings"


def test_get_book_by_id(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    retrieved_book = service.get_book_by_id(book.id)

    assert retrieved_book is not None
    assert retrieved_book.title == "The Hobbit"


def test_get_book_by_isbn(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    retrieved_book = service.get_book_by_isbn(
        "9780547928227"
    )

    assert retrieved_book is not None
    assert retrieved_book.id == book.id


def test_search_books(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    service.create_book(
        title="The Lord of the Rings",
        isbn="9780618640157",
        publication_year=1954,
        genre="Fantasy",
        author_id=author.id,
    )

    results = service.search_books("Hobbit")

    assert len(results) == 1
    assert results[0].title == "The Hobbit"


def test_update_book(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book.title = "The Hobbit: Revised Edition"

    updated_book = service.update_book(book)

    assert updated_book.title == "The Hobbit: Revised Edition"


def test_delete_book(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book_id = book.id

    service.delete_book(book)

    assert service.get_book_by_id(book_id) is None

def test_create_book_rejects_blank_title(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    with pytest.raises(ValueError, match="Title cannot be blank"):
        service.create_book(
            title="",
            isbn="9780547928227",
            publication_year=1937,
            genre="Fantasy",
            author_id=author.id,
        )

def test_create_book_rejects_blank_isbn(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    with pytest.raises(ValueError, match="ISBN cannot be blank"):
        service.create_book(
            title="The Hobbit",
            isbn="",
            publication_year=1937,
            genre="Fantasy",
            author_id=author.id,
        )

def test_create_book_rejects_duplicate_isbn(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    with pytest.raises(ValueError, match="A book with this ISBN already exists"):
        service.create_book(
            title="Another Book",
            isbn="9780547928227",
            publication_year=2000,
            genre="Fantasy",
            author_id=author.id,
        )

def test_update_book_rejects_duplicate_isbn(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book_one = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book_two = service.create_book(
        title="The Lord of the Rings",
        isbn="9780618640157",
        publication_year=1954,
        genre="Fantasy",
        author_id=author.id,
    )

    book_two.isbn = book_one.isbn

    with pytest.raises(ValueError, match="A book with this ISBN already exists"):
        service.update_book(book_two)

def test_update_book_rejects_blank_title(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book.title = "   "

    with pytest.raises(ValueError, match="Title cannot be blank"):
        service.update_book(book)

def test_update_book_rejects_blank_isbn(db_session):
    author = create_author(db_session)
    service = BookService(db_session)

    book = service.create_book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book.isbn = "   "

    with pytest.raises(ValueError, match="ISBN cannot be blank"):
        service.update_book(book)