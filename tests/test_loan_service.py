from datetime import date

import pytest

from app.database.models import Author, Book, BookCopy, Member
from app.services.loan_service import LoanService


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
        status="AVAILABLE",
    )
    member = Member(
        first_name="Bilbo",
        last_name="Baggins",
        email="bilbo@example.com",
    )

    db_session.add_all([book_copy, member])
    db_session.commit()

    db_session.refresh(book_copy)
    db_session.refresh(member)

    return book_copy, member


def test_create_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    assert loan.id is not None
    assert loan.copy_id == book_copy.id
    assert loan.member_id == member.id
    assert loan.status == "ACTIVE"
    assert loan.checkout_date == date.today()
    assert loan.due_date == date.fromordinal(
        date.today().toordinal() + 14
    )

def test_create_loan_rejects_nonexistent_copy(db_session):
    _, member = create_loan_data(db_session)

    service = LoanService(db_session)

    with pytest.raises(
        ValueError,
        match="Book copy not found",
    ):
        service.create_loan(
            copy_id=999,
            member_id=member.id,
        )


def test_create_loan_custom_period(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
        loan_period_days=21,
    )

    assert loan.due_date == date.fromordinal(
        date.today().toordinal() + 21
    )


def test_create_loan_rejects_active_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    with pytest.raises(
        ValueError,
        match="This book copy is already loaned out",
    ):
        service.create_loan(
            copy_id=book_copy.id,
            member_id=member.id,
        )


def test_create_loan_rejects_invalid_period(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    with pytest.raises(
        ValueError,
        match="Loan period must be greater than zero",
    ):
        service.create_loan(
            copy_id=book_copy.id,
            member_id=member.id,
            loan_period_days=0,
        )


def test_get_active_loan_for_copy(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    result = service.get_active_loan_for_copy(book_copy.id)

    assert result is not None
    assert result.id == loan.id


def test_return_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    returned_loan = service.return_loan(loan)

    assert returned_loan.status == "RETURNED"
    assert returned_loan.return_date == date.today()


def test_return_loan_rejects_non_active_loan(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    service.return_loan(loan)

    with pytest.raises(
        ValueError,
        match="This loan is not active",
    ):
        service.return_loan(loan)

def test_create_loan_rejects_archived_member(db_session):
    book_copy, member = create_loan_data(db_session)

    member.is_archived = True
    db_session.commit()

    service = LoanService(db_session)

    with pytest.raises(
        ValueError,
        match="Cannot loan a book to an archived member",
    ):
        service.create_loan(
            copy_id=book_copy.id,
            member_id=member.id,
        )

def test_create_loan_rejects_archived_book(db_session):
    book_copy, member = create_loan_data(db_session)

    book_copy.book.is_archived = True
    db_session.commit()

    service = LoanService(db_session)

    with pytest.raises(
        ValueError,
        match="Cannot loan a copy of an archived book",
    ):
        service.create_loan(
            copy_id=book_copy.id,
            member_id=member.id,
        )

def test_create_loan_marks_copy_as_loaned(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    assert book_copy.status == "LOANED"

def test_return_loan_marks_copy_as_available(db_session):
    book_copy, member = create_loan_data(db_session)

    service = LoanService(db_session)

    loan = service.create_loan(
        copy_id=book_copy.id,
        member_id=member.id,
    )

    assert book_copy.status == "LOANED"

    service.return_loan(loan)

    assert book_copy.status == "AVAILABLE"