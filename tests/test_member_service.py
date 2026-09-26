from datetime import date

import pytest

from app.services.member_service import MemberService


def test_create_member(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        phone="555-1234",
    )

    assert member.id is not None
    assert member.first_name == "John"
    assert member.last_name == "Smith"
    assert member.email == "john@example.com"
    assert member.phone == "555-1234"
    assert member.membership_date == date.today()


def test_create_member_strips_whitespace(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="  John  ",
        last_name="  Smith  ",
        email="  john@example.com  ",
        phone=" 555-1234 ",
    )

    assert member.first_name == "John"
    assert member.last_name == "Smith"
    assert member.email == "john@example.com"
    assert member.phone == "555-1234"


def test_create_member_rejects_blank_first_name(db_session):
    service = MemberService(db_session)

    with pytest.raises(ValueError, match="First name cannot be blank"):
        service.create_member(
            first_name="",
            last_name="Smith",
            email="john@example.com",
        )


def test_create_member_rejects_blank_last_name(db_session):
    service = MemberService(db_session)

    with pytest.raises(ValueError, match="Last name cannot be blank"):
        service.create_member(
            first_name="John",
            last_name="",
            email="john@example.com",
        )


def test_create_member_rejects_blank_email(db_session):
    service = MemberService(db_session)

    with pytest.raises(ValueError, match="Email cannot be blank"):
        service.create_member(
            first_name="John",
            last_name="Smith",
            email="",
        )


def test_create_member_rejects_duplicate_email(db_session):
    service = MemberService(db_session)

    service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    with pytest.raises(
        ValueError,
        match="A member with this email already exists",
    ):
        service.create_member(
            first_name="Jane",
            last_name="Doe",
            email="john@example.com",
        )


def test_get_all_members(db_session):
    service = MemberService(db_session)

    service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )
    service.create_member(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
    )

    members = service.get_all_members()

    assert len(members) == 2


def test_get_member_by_id(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    result = service.get_member_by_id(member.id)

    assert result is not None
    assert result.id == member.id


def test_get_member_by_email(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    result = service.get_member_by_email("john@example.com")

    assert result is not None
    assert result.id == member.id


def test_update_member(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        phone="555-1234",
    )

    member.first_name = "Jonathan"
    member.phone = "555-5678"

    updated_member = service.update_member(member)

    assert updated_member.first_name == "Jonathan"
    assert updated_member.phone == "555-5678"


def test_update_member_rejects_duplicate_email(db_session):
    service = MemberService(db_session)

    member_1 = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    service.create_member(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
    )

    member_1.email = "jane@example.com"

    with pytest.raises(
        ValueError,
        match="A member with this email already exists",
    ):
        service.update_member(member_1)


def test_delete_member(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    service.archive_member(member)

    archived_member = service.get_member_by_id(member.id)

    assert archived_member is not None
    assert archived_member.id == member.id
    assert archived_member.is_archived is True

def test_create_member_rejects_invalid_email(db_session):
    service = MemberService(db_session)

    with pytest.raises(ValueError, match="Invalid email format"):
        service.create_member(
            first_name="John",
            last_name="Smith",
            email="john@example",
        )


def test_create_member_accepts_valid_email(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
    )

    assert member.email == "john.smith@example.com"


def test_create_member_rejects_invalid_phone(db_session):
    service = MemberService(db_session)

    with pytest.raises(ValueError, match="Invalid phone number format"):
        service.create_member(
            first_name="John",
            last_name="Smith",
            email="john@example.com",
            phone="123-456",
        )


def test_create_member_accepts_valid_phone(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        phone="555-123-4567",
    )

    assert member.phone == "555-123-4567"

def test_archive_member(db_session):
    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    service.archive_member(member)

    assert member.is_archived is True

def test_archived_member_is_not_returned_by_get_all(db_session):
    service = MemberService(db_session)

    active_member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    archived_member = service.create_member(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
    )

    service.archive_member(archived_member)

    members = service.get_all_members()

    assert len(members) == 1
    assert members[0].id == active_member.id

def test_archive_member_rejects_active_loan(db_session):
    from app.database.models import BookCopy, Loan

    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    book_copy = BookCopy(
        book_id=1,
        status="LOANED",
    )
    db_session.add(book_copy)
    db_session.flush()

    loan = Loan(
        copy_id=book_copy.id,
        member_id=member.id,
        status="ACTIVE",
        checkout_date=date.today(),
        due_date=date.today(),
    )
    db_session.add(loan)
    db_session.commit()

    with pytest.raises(
        ValueError,
        match="Cannot archive a member while they have an active loan",
    ):
        service.archive_member(member)

    assert member.is_archived is False

def test_archive_member_allows_returned_loans(db_session):
    from app.database.models import BookCopy, Loan

    service = MemberService(db_session)

    member = service.create_member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    book_copy = BookCopy(
        book_id=1,
        status="AVAILABLE",
    )
    db_session.add(book_copy)
    db_session.flush()

    loan = Loan(
        copy_id=book_copy.id,
        member_id=member.id,
        status="RETURNED",
        checkout_date=date.today(),
        due_date=date.today(),
        return_date=date.today(),
    )
    db_session.add(loan)
    db_session.commit()

    service.archive_member(member)

    assert member.is_archived is True