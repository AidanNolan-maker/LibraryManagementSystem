import re

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
)

class AddMemberDialog(QDialog):
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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Member")
        self.setMinimumWidth(400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Enter first name")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Enter last name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_and_accept(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        if not first_name:
            QMessageBox.warning(
                self,
                "Invalid Member",
                "First name cannot be blank."
            )
            self.first_name_input.setFocus()
            return

        if not last_name:
            QMessageBox.warning(
                self,
                "Invald Member",
                "Last name cannot be blank."
            )
            self.last_name_input.setFocus()
            return

        if not email:
            QMessageBox.warning(
                self,
                "Invalid Member",
                "Email cannot be blank.",
            )
            self.email_input.setFocus()
            return

        if not self.EMAIL_PATTERN.fullmatch(email):
            QMessageBox.warning(
                self,
                "Invalid Member",
                "Please enter a valid email address.",
            )
            self.email_input.setFocus()
            return

        if phone and not self.PHONE_PATTERN.fullmatch(phone):
            QMessageBox.warning(
                self,
                "Invalid Member",
                "Please enter a valid phone number."
            )
            self.phone_input.setFocus()
            return

        self.accept()

    def get_member_data(self):
        return {
            "first_name": self.first_name_input.text(),
            "last_name": self.last_name_input.text(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
        }