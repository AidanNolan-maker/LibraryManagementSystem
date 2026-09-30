from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Member

class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Member]:
        statement = (
            select(Member)
            .where(Member.is_archived.is_(False))
            .order_by(Member.last_name, Member.first_name)
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, member_id: int) -> Member | None:
        return self.db.get(Member, member_id)

    def get_by_email(self, email: str) -> Member | None:
        statement = select(Member).where(Member.email == email)
        return self.db.scalars(statement).first()

    def create(self, member: Member) -> Member:
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def update(self, member: Member) -> Member:
        self.db.commit()
        self.db.refresh(member)
        return member

    def delete(self, member: Member) -> None:
        self.db.delete(member)
        self.db.commit()

    def search(self, search_term: str):
        search_pattern = f"%{search_term}%"

        statement = select(Member).where(
            Member.is_archived.is_(False),
            (
                Member.first_name.ilike(search_pattern)
                | Member.last_name.ilike(search_pattern)
                | Member.email.ilike(search_pattern)
                | Member.phone.ilike(search_pattern)
            ),
        ).order_by(Member.last_name, Member.first_name)

        return list(self.db.scalars(statement).all())