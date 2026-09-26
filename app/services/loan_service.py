from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.database.models import Loan
from app.repositories.book_copy_repository import BookCopyRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.member_repository import MemberRepository

class LoanService:
    def __init__(self, db: Session):
        self.repository = LoanRepository(db)
        self.book_copy_repository = BookCopyRepository(db)
        self.member_repository = MemberRepository(db)

    def get_all_loans(self) -> list[Loan]:
        return self.repository.get_all()

    def get_loan_by_id(self, loan_id: int) -> Loan | None:
        return self.repository.get_by_id(loan_id)

    def get_loans_for_copy(self, copy_id: int) -> list[Loan]:
        return self.repository.get_by_copy_id(copy_id)

    def get_active_loan_for_copy(self, copy_id: int) -> Loan | None:
        return self.repository.get_active_by_copy_id(copy_id)

    def create_loan(
            self,
            copy_id: int,
            member_id: int,
            loan_period_days: int = 14,
    ) -> Loan:
        book_copy = self.book_copy_repository.get_by_id(copy_id)

        if book_copy is None:
            raise ValueError("Book copy not found")

        if book_copy.book.is_archived:
            raise ValueError("Cannot loan a copy of an archived book")

        member = self.member_repository.get_by_id(member_id)

        if member is None:
            raise ValueError("Member not found")

        if member.is_archived:
            raise ValueError("Cannot loan a book to an archived member")

        if self.get_active_loan_for_copy(copy_id) is not None:
            raise ValueError("This book copy is already loaned out")

        if book_copy.status != "AVAILABLE":
            raise ValueError("This book copy is not available")

        if loan_period_days <= 0:
            raise ValueError("Loan period must be greater than zero")

        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=loan_period_days)

        loan = Loan(
            copy_id=copy_id,
            member_id=member_id,
            checkout_date=checkout_date,
            due_date=due_date,
            status="ACTIVE",
        )

        book_copy.status = "LOANED"

        loan = self.repository.create(loan)

        return loan

    def return_loan(self, loan: Loan) -> Loan:
        if loan.status != "ACTIVE":
            raise ValueError("This loan is not active")

        loan.status = "RETURNED"
        loan.return_date = date.today()

        book_copy = self.book_copy_repository.get_by_id(loan.copy_id)

        if book_copy is None:
            raise ValueError("Book copy not found")

        book_copy.status = "AVAILABLE"

        return self.repository.update(loan)

    def delete_loan(self, loan: Loan) -> None:
        self.repository.delete(loan)