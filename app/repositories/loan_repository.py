from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Loan

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Loan]:
        statement = select(Loan).order_by(Loan.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, loan_id: int) -> Loan | None:
        return self.db.get(Loan, loan_id)

    def get_by_copy_id(self, copy_id: int) -> list[Loan]:
        statement = (
            select(Loan)
            .where(Loan.copy_id == copy_id)
            .order_by(Loan.id)
        )
        return list(self.db.scalars(statement).all())

    def get_active_by_copy_id(self, copy_id: int) -> Loan | None:
        statement = (
            select(Loan)
            .where(
                Loan.copy_id == copy_id,
                Loan.status == "ACTIVE",
            )
        )
        return self.db.scalars(statement).first()

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def update(self, loan: Loan) -> Loan:
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def delete(self, loan: Loan) -> None:
        self.db.delete(loan)
        self.db.commit()