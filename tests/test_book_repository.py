from app.database.models import Author, Book
from app.repositories.book_repository import BookRepository

def create_author(db_session):
    author = Author(
        first_name="J.R.R.",
        last_name="Tolkien",
    )

    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    return author

def create_book(
        db_session,
        author,
        title="The Hobbit",
        isbn="9780547928227",
):
    book = Book(
        title=title,
        isbn=isbn,
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
    )

    repository = BookRepository(db_session)

    return repository.create(book)

def test_create_and_get_book(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    book = create_book(db_session, author)

    assert book.id is not None
    assert book.title == "The Hobbit"

    retrieved_book = repository.get_by_id(book.id)

    assert retrieved_book is not None
    assert retrieved_book.title == "The Hobbit"
    assert retrieved_book.isbn == "9780547928227"

def test_get_all_books(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    create_book(
        db_session,
        author,
        title="The Hobbit",
        isbn="9780547928227",
    )

    create_book(
        db_session,
        author,
        title="The Lord of the Rings",
        isbn="9780618640157",
    )

    books = repository.get_all()

    assert len(books) == 2
    assert books[0].title == "The Hobbit"
    assert books[1].title == "The Lord of the Rings"

def test_get_book_by_isbn(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    book = create_book(
        db_session,
        author,
        isbn="9780547928227",
    )

    retrieved_book = repository.get_by_isbn("9780547928227")

    assert retrieved_book is not None
    assert retrieved_book.id == book.id

def test_search_books_by_title(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    create_book(
        db_session,
        author,
        title="The Hobbit",
        isbn="9780547928227",
    )

    create_book(
        db_session,
        author,
        title="The Lord of the Rings",
        isbn="9780618640157",
    )

    results = repository.search("Hobbit")

    assert len(results) == 1
    assert results[0].title == "The Hobbit"

def test_update_book(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    book = create_book(db_session, author)

    book.title = "The Hobbit: Revised Edition"

    updated_book = repository.update(book)

    assert updated_book.title == "The Hobbit: Revised Edition"

    retrieved_book = repository.get_by_id(book.id)

    assert retrieved_book is not None
    assert retrieved_book.title == "The Hobbit: Revised Edition"

def test_delete_book(db_session):
    author = create_author(db_session)
    repository = BookRepository(db_session)

    book = create_book(db_session, author)

    book_id = book.id

    repository.delete(book)

    retrieved_book = repository.get_by_id(book_id)

    assert retrieved_book is None

def test_get_all_excludes_archived_books(db_session):
    author = create_author(db_session)

    active_book = Book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
        is_archived=False,
    )

    archived_book = Book(
        title="The Silmarillion",
        isbn="9780261102736",
        publication_year=1977,
        genre="Fantasy",
        author_id=author.id,
        is_archived=True,
    )

    db_session.add_all([active_book, archived_book])
    db_session.commit()

    repository = BookRepository(db_session)

    books = repository.get_all()

    assert len(books) == 1
    assert books[0].title == "The Hobbit"


def test_search_excludes_archived_books(db_session):
    author = create_author(db_session)

    active_book = Book(
        title="The Hobbit",
        isbn="9780547928227",
        publication_year=1937,
        genre="Fantasy",
        author_id=author.id,
        is_archived=False,
    )

    archived_book = Book(
        title="The Hobbit: Annotated Edition",
        isbn="9780000000001",
        publication_year=2000,
        genre="Fantasy",
        author_id=author.id,
        is_archived=True,
    )

    db_session.add_all([active_book, archived_book])
    db_session.commit()

    repository = BookRepository(db_session)

    books = repository.search("Hobbit")

    assert len(books) == 1
    assert books[0].title == "The Hobbit"


def test_get_by_id_includes_archived_books(db_session):
    author = create_author(db_session)

    book = Book(
        title="The Silmarillion",
        isbn="9780261102736",
        publication_year=1977,
        genre="Fantasy",
        author_id=author.id,
        is_archived=True,
    )

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    repository = BookRepository(db_session)

    result = repository.get_by_id(book.id)

    assert result is not None
    assert result.is_archived is True