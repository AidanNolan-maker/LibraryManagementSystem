import pytest

from app.database.models import Author, Book
from app.services.book_copy_service import BookCopyService


def create_book(db_session):
    author = Author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    book = Book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    return book


def test_get_all_copies(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    service.create_copy(book.id)
    service.create_copy(book.id)

    copies = service.get_all_copies()

    assert len(copies) == 2


def test_get_copy_by_id(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    copy = service.create_copy(book.id)

    result = service.get_copy_by_id(copy.id)

    assert result is not None
    assert result.id == copy.id


def test_get_copies_for_book(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    service.create_copy(book.id)
    service.create_copy(book.id)

    copies = service.get_copies_for_book(book.id)

    assert len(copies) == 2
    assert all(copy.book_id == book.id for copy in copies)


def test_create_copy_defaults_to_available(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)

    copy = service.create_copy(book.id)

    assert copy.id is not None
    assert copy.book_id == book.id
    assert copy.status == "AVAILABLE"


def test_update_copy(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    copy = service.create_copy(book.id)

    copy.status = "LOANED"

    updated_copy = service.update_copy(copy)

    assert updated_copy.status == "LOANED"


def test_update_copy_rejects_invalid_status(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    copy = service.create_copy(book.id)

    copy.status = "INVALID"

    with pytest.raises(ValueError, match="Invalid book copy status"):
        service.update_copy(copy)


def test_delete_copy(db_session):
    book = create_book(db_session)

    service = BookCopyService(db_session)
    copy = service.create_copy(book.id)

    service.delete_copy(copy)

    assert service.get_copy_by_id(copy.id) is None

def test_get_copies_for_book_only_returns_matching_book(db_session):
    author = Author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    book_one = Book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    book_two = Book(
        title="The Lord of the Rings",
        isbn="9780261102385",
        publication_year=1954,
        genre="Fantasy",
        author_id=author.id,
    )

    db_session.add_all([book_one, book_two])
    db_session.commit()
    db_session.refresh(book_one)
    db_session.refresh(book_two)

    service = BookCopyService(db_session)

    service.create_copy(book_one.id)
    service.create_copy(book_one.id)
    service.create_copy(book_two.id)

    copies = service.get_copies_for_book(book_one.id)

    assert len(copies) == 2
    assert all(copy.book_id == book_one.id for copy in copies)