from datetime import date

from app.database.models import Member
from app.repositories.member_repository import MemberRepository


def test_get_all_members(db_session):
    repository = MemberRepository(db_session)

    member_1 = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        phone="555-1111",
        membership_date=date(2026, 9, 1),
    )
    member_2 = Member(
        first_name="Jane",
        last_name="Adams",
        email="jane@example.com",
        phone="555-2222",
        membership_date=date(2026, 9, 2),
    )

    db_session.add_all([member_1, member_2])
    db_session.commit()

    members = repository.get_all()

    assert len(members) == 2
    assert members[0].last_name == "Adams"
    assert members[1].last_name == "Smith"


def test_get_member_by_id(db_session):
    repository = MemberRepository(db_session)

    member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
    )
    db_session.add(member)
    db_session.commit()

    result = repository.get_by_id(member.id)

    assert result is not None
    assert result.id == member.id
    assert result.email == "john@example.com"


def test_get_member_by_id_returns_none_for_missing_member(db_session):
    repository = MemberRepository(db_session)

    result = repository.get_by_id(999)

    assert result is None


def test_get_member_by_email(db_session):
    repository = MemberRepository(db_session)

    member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
    )
    db_session.add(member)
    db_session.commit()

    result = repository.get_by_email("john@example.com")

    assert result is not None
    assert result.id == member.id


def test_get_member_by_email_returns_none_for_missing_email(db_session):
    repository = MemberRepository(db_session)

    result = repository.get_by_email("missing@example.com")

    assert result is None


def test_create_member(db_session):
    repository = MemberRepository(db_session)

    member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
    )

    result = repository.create(member)

    assert result.id is not None
    assert result.first_name == "John"
    assert result.last_name == "Smith"
    assert result.email == "john@example.com"


def test_update_member(db_session):
    repository = MemberRepository(db_session)

    member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
    )
    db_session.add(member)
    db_session.commit()

    member.first_name = "Jonathan"

    result = repository.update(member)

    assert result.first_name == "Jonathan"


def test_delete_member(db_session):
    repository = MemberRepository(db_session)

    member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
    )
    db_session.add(member)
    db_session.commit()

    repository.delete(member)

    assert repository.get_by_id(member.id) is None

def test_get_all_members_excludes_archived_members(db_session):
    repository = MemberRepository(db_session)

    active_member = Member(
        first_name="John",
        last_name="Smith",
        email="john@example.com",
        membership_date=date(2026, 9, 1),
        is_archived=False,
    )

    archived_member = Member(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        membership_date=date(2026, 9, 2),
        is_archived=True,
    )

    db_session.add_all([active_member, archived_member])
    db_session.commit()

    members = repository.get_all()

    assert len(members) == 1
    assert members[0].email == "john@example.com"