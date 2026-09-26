from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
)

from app.database.database import SessionLocal
from app.services.book_copy_service import BookCopyService
from app.services.loan_service import LoanService
from app.services.member_service import MemberService

class CheckoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Check Out Book")
        self.setMinimumWidth(450)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.copy_combo = QComboBox()
        self.member_combo = QComboBox()

        self.loan_period_input = QSpinBox()
        self.loan_period_input.setMinimum(1)
        self.loan_period_input.setMaximum(365)
        self.loan_period_input.setValue(14)

        form_layout.addRow("Book Copy:", self.copy_combo)
        form_layout.addRow("Member:", self.member_combo)
        form_layout.addRow("Loan Period (days):", self.loan_period_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.button(
            QDialogButtonBox.StandardButton.Ok
        ).clicked.connect(self.checkout)

        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

    def load_data(self):
        db = SessionLocal()

        try:
            copy_service = BookCopyService(db)
            member_service = MemberService(db)

            copies = copy_service.get_all_copies()
            members = member_service.get_all_members()

            for book_copy in copies:
                if book_copy.status != "AVAILABLE":
                    continue

                self.copy_combo.addItem(
                    f"Copy {book_copy.id} - {book_copy.book.title}",
                    book_copy.id,
                )

            for member in members:
                self.member_combo.addItem(
                    f"{member.first_name} {member.last_name} - {member.email}",
                    member.id,
                )

        finally:
            db.close()

    def checkout(self):
        copy_id = self.copy_combo.currentData()
        member_id = self.member_combo.currentData()
        loan_period_days = self.loan_period_input.value()

        if copy_id is None:
            QMessageBox.warning(
                self,
                "Unable to Check Out Book",
                "No available book copies were found.",
            )
            return

        if member_id is None:
            QMessageBox.warning(
                self,
                "Unable to Check Out Book",
                "No active members were found.",
            )
            return

        db = SessionLocal()

        try:
            service = LoanService(db)

            service.create_loan(
                copy_id=copy_id,
                member_id=member_id,
                loan_period_days=loan_period_days,
            )

            self.accept()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to Check Out Book",
                str(error),
            )

        finally:
            db.close()