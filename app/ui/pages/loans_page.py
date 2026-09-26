from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
)

from app.database.database import SessionLocal
from app.services.loan_service import LoanService
from app.ui.pages.checkout_dialog import CheckoutDialog

class LoansPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_loans()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Loans")
        title.setObjectName("page_title")

        self.checkout_button = QPushButton("Check Out Book")
        self.checkout_button.clicked.connect(self.open_checkout_dialog)

        self.return_button = QPushButton("Return Book")
        self.return_button.clicked.connect(self.return_selected_loan)

        self.loan_table = QTableWidget()
        self.loan_table.setColumnCount(8)
        self.loan_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Copy ID",
                "Book",
                "Member",
                "Checkout Date",
                "Due Date",
                "Return Date",
                "Status",
            ]
        )

        self.loan_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.loan_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.loan_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.loan_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(title)
        layout.addWidget(self.checkout_button)
        layout.addWidget(self.return_button)
        layout.addWidget(self.loan_table)

    def load_loans(self):
        db = SessionLocal()

        try:
            service = LoanService(db)
            loans = service.get_all_loans()

            self.loan_table.setRowCount(len(loans))

            for row, loan in enumerate(loans):
                self.loan_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(str(loan.id)),
                )
                self.loan_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(loan.copy_id)),
                )
                self.loan_table.setItem(
                    row,
                    2,
                    QTableWidgetItem(loan.book_copy.book.title),
                )
                self.loan_table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        f"{loan.member.first_name} {loan.member.last_name}"
                    ),
                )
                self.loan_table.setItem(
                    row,
                    4,
                    QTableWidgetItem(
                        loan.checkout_date.strftime("%Y-%m-%d")
                    ),
                )
                self.loan_table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        loan.due_date.strftime("%Y-%m-%d")
                    ),
                )
                self.loan_table.setItem(
                    row,
                    6,
                    QTableWidgetItem(
                        loan.return_date.strftime("%Y-%m-%d")
                        if loan.return_date
                        else ""
                    ),
                )
                self.loan_table.setItem(
                    row,
                    7,
                    QTableWidgetItem(loan.status),
                )

        finally:
            db.close()

    def open_checkout_dialog(self):
        dialog = CheckoutDialog(self)

        if dialog.exec() == dialog.DialogCode.Accepted:
            self.loan_table.clearContents()
            self.load_loans()

    def return_selected_loan(self):
        selected_rows = self.loan_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Loan Selected",
                "Please select a loan to return.",
            )
            return

        row = selected_rows[0].row()

        loan_id_item = self.loan_table.item(row, 0)

        if loan_id_item is None:
            QMessageBox.warning(
                self,
                "Invalid Selection",
                "The selected loan does not have a valid ID.",
            )
            return

        loan_id = int(loan_id_item.text())

        db = SessionLocal()

        try:
            service = LoanService(db)
            loan = service.get_loan_by_id(loan_id)

            if loan is None:
                QMessageBox.warning(
                    self,
                    "Loan Not Found",
                    "The selected loan could not be found.",
                )
                return

            if loan.status != "ACTIVE":
                QMessageBox.warning(
                    self,
                    "Loan Already Returned",
                    "The selected loan is not currently active.",
                )
                return

            confirmation = QMessageBox.question(
                self,
                "Return Book",
                f"Are you sure you want to return loan #{loan.id}?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if confirmation != QMessageBox.StandardButton.Yes:
                return

            service.return_loan(loan)

            self.loan_table.clearContents()
            self.load_loans()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to Return Book",
                str(error),
            )

        finally:
            db.close()