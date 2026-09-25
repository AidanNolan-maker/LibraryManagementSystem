from datetime import date, timedelta

from app.database.models import Author, Book, BookCopy, Loan, Member
from app.repositories.loan_repository import LoanRepository


def create_loan_data(db_session):
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

    book_copy = BookCopy(
        book_id=book.id,
        status="LOANED",
    )
    db_session.add(book_copy)

    member = Member(
        first_name="Bilbo",
        last_name="Baggins",
        email="bilbo@example.com",
    )
    db_session.add(member)
    db_session.commit()

    db_session.refresh(book_copy)
    db_session.refresh(member)

    return book_copy, member


def create_loan(db_session, copy_id, member_id, status="ACTIVE"):
    loan = Loan(
        copy_id=copy_id,
        member_id=member_id,
        checkout_date=date.today(),
        due_date=date.today() + timedelta(days=14),
        status=status,
    )
    db_session.add(loan)
    db_session.commit()
    db_session.refresh(loan)

    return loan


def test_get_all_loans(db_session):
    book_copy, member = create_loan_data(db_session)

    create_loan(db_session, book_copy.id, member.id)

    repository = LoanRepository(db_session)

    loans = repository.get_all()

    assert len(loans) == 1
    assert loans[0].copy_id == book_copy.id
    assert loans[0].member_id == member.id


def test_get_by_id(db_session):
    book_copy, member = create_loan_data(db_session)

    loan = create_loan(db_session, book_copy.id, member.id)

    repository = LoanRepository(db_session)

    result = repository.get_by_id(loan.id)

    assert result is not None
    assert result.id == loan.id


def test_get_by_copy_id(db_session):
    book_copy, member = create_loan_data(db_session)

    create_loan(db_session, book_copy.id, member.id, "ACTIVE")
    create_loan(db_session, book_copy.id, member.id, "RETURNED")

    repository = LoanRepository(db_session)

    loans = repository.get_by_copy_id(book_copy.id)

    assert len(loans) == 2
    assert all(loan.copy_id == book_copy.id for loan in loans)


def test_get_active_by_copy_id_returns_active_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    loan = create_loan(
        db_session,
        book_copy.id,
        member.id,
        "ACTIVE",
    )

    repository = LoanRepository(db_session)

    result = repository.get_active_by_copy_id(book_copy.id)

    assert result is not None
    assert result.id == loan.id
    assert result.status == "ACTIVE"


def test_get_active_by_copy_id_ignores_returned_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    create_loan(
        db_session,
        book_copy.id,
        member.id,
        "RETURNED",
    )

    repository = LoanRepository(db_session)

    result = repository.get_active_by_copy_id(book_copy.id)

    assert result is None


def test_create_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    repository = LoanRepository(db_session)

    loan = repository.create(
        Loan(
            copy_id=book_copy.id,
            member_id=member.id,
            checkout_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status="ACTIVE",
        )
    )

    assert loan.id is not None
    assert loan.copy_id == book_copy.id
    assert loan.member_id == member.id
    assert loan.status == "ACTIVE"


def test_update_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    repository = LoanRepository(db_session)

    loan = create_loan(
        db_session,
        book_copy.id,
        member.id,
    )

    loan.status = "RETURNED"
    loan.return_date = date.today()

    updated_loan = repository.update(loan)

    assert updated_loan.status == "RETURNED"
    assert updated_loan.return_date == date.today()


def test_delete_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    repository = LoanRepository(db_session)

    loan = create_loan(
        db_session,
        book_copy.id,
        member.id,
    )

    repository.delete(loan)

    assert repository.get_by_id(loan.id) is None

