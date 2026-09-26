import re

from datetime import date

from sqlalchemy.orm import Session

from app.database.models import Member
from app.repositories.member_repository import MemberRepository
from app.repositories.loan_repository import LoanRepository

class MemberService:
    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_PATTERN = re.compile(
        r"^(?:"
        r"\d{7}"
        r"|\d{3}[-.]\d{4}"
        r"|\d{10}"
        r"|\d{3}[-.]\d{3}[-.]\d{4}"
        r"|\(\d{3}\) \d{3}-\d{4}"
        r")$"
    )

    def __init__(self, db: Session):
        self.repository = MemberRepository(db)
        self.loan_repository = LoanRepository(db)

    def get_all_members(self) -> list[Member]:
        return self.repository.get_all()

    def get_member_by_id(self, member_id: int) -> Member | None:
        return self.repository.get_by_id(member_id)

    def get_member_by_email(self, email: str) -> Member | None:
        return self.repository.get_by_email(email)

    def create_member(
            self,
            first_name: str,
            last_name: str,
            email: str,
            phone: str | None = None,
    ) -> Member:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()
        phone = phone.strip() if phone else None

        if not first_name:
            raise ValueError("First name cannot be blank")

        if not last_name:
            raise ValueError("Last name cannot be blank")

        if not email:
            raise ValueError("Email cannot be blank")

        if not self.EMAIL_PATTERN.fullmatch(email):
            raise ValueError("Invalid email format")

        if phone and not self.PHONE_PATTERN.fullmatch(phone):
            raise ValueError("Invalid phone number format")

        if self.repository.get_by_email(email) is not None:
            raise ValueError("A member with this email already exists")

        member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            membership_date=date.today()
        )

        return self.repository.create(member)

    def update_member(self, member: Member) -> Member:
        with self.repository.db.no_autoflush:
            first_name = member.first_name.strip()
            last_name = member.last_name.strip()
            email = member.email.strip()
            phone = member.phone.strip() if member.phone else None

            if not first_name:
                raise ValueError("First name cannot be blank")

            if not last_name:
                raise ValueError("Last name cannot be blank")

            if not email:
                raise ValueError("Email cannot be blank")

            if not self.EMAIL_PATTERN.fullmatch(email):
                raise ValueError("Invalid email format")

            if phone and not self.PHONE_PATTERN.fullmatch(phone):
                raise ValueError("Invalid phone number format")

            existing_member = self.repository.get_by_email(email)

            if existing_member is not None and existing_member.id != member.id:
                raise ValueError("A member with this email already exists")

            member.first_name = first_name
            member.last_name = last_name
            member.email = email
            member.phone = phone

        return self.repository.update(member)

    def archive_member(self, member: Member) -> None:
        for loan in member.loans:
            if loan.status == "ACTIVE":
                raise ValueError(
                    "Cannot archive a member while they have an active loan"
                )

        member.is_archived = True
        self.repository.update(member)