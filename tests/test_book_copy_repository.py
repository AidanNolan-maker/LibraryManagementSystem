from app.database.models import Author, Book, BookCopy
from app.repositories.book_copy_repository import BookCopyRepository


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


def test_get_all_book_copies(db_session):
    book = create_book(db_session)

    copy = BookCopy(book_id=book.id)
    db_session.add(copy)
    db_session.commit()

    repository = BookCopyRepository(db_session)

    copies = repository.get_all()

    assert len(copies) == 1
    assert copies[0].book_id == book.id


def test_get_by_id(db_session):
    book = create_book(db_session)

    copy = BookCopy(book_id=book.id)
    db_session.add(copy)
    db_session.commit()
    db_session.refresh(copy)

    repository = BookCopyRepository(db_session)

    result = repository.get_by_id(copy.id)

    assert result is not None
    assert result.id == copy.id


def test_get_by_book_id(db_session):
    book = create_book(db_session)

    db_session.add_all([
        BookCopy(book_id=book.id),
        BookCopy(book_id=book.id),
    ])
    db_session.commit()

    repository = BookCopyRepository(db_session)

    copies = repository.get_by_book_id(book.id)

    assert len(copies) == 2
    assert all(copy.book_id == book.id for copy in copies)


def test_create_book_copy(db_session):
    book = create_book(db_session)

    repository = BookCopyRepository(db_session)

    copy = repository.create(
        BookCopy(book_id=book.id)
    )

    assert copy.id is not None
    assert copy.book_id == book.id
    assert copy.status == "AVAILABLE"


def test_update_book_copy(db_session):
    book = create_book(db_session)

    repository = BookCopyRepository(db_session)

    copy = repository.create(
        BookCopy(book_id=book.id)
    )

    copy.status = "LOANED"

    updated_copy = repository.update(copy)

    assert updated_copy.status == "LOANED"


def test_delete_book_copy(db_session):
    book = create_book(db_session)

    repository = BookCopyRepository(db_session)

    copy = repository.create(
        BookCopy(book_id=book.id)
    )

    repository.delete(copy)

    assert repository.get_by_id(copy.id) is None