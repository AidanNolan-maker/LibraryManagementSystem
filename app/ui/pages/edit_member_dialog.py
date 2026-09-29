from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
)

from app.database.models import Member

class EditMemberDialog(QDialog):
    save_requested = Signal(dict)

    def __init__(self, member: Member, parent=None):
        super().__init__(parent)

        self.member = member

        self.setWindowTitle("Edit Member")
        self.setMinimumWidth(400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setText(self.member.first_name)

        self.last_name_input = QLineEdit()
        self.last_name_input.setText(self.member.last_name)

        self.email_input = QLineEdit()
        self.email_input.setText(self.member.email)

        self.phone_input = QLineEdit()
        self.phone_input.setText(self.member.phone or "")

        form_layout.addRow("First Name:", self.first_name_input)
        form_layout.addRow("Last Name:", self.last_name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Phone:", self.phone_input)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.button_box.button(
            QDialogButtonBox.StandardButton.Ok
        ).clicked.connect(self.validate_and_submit)
        self.button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def validate_and_submit(self):
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        if not first_name:
            QMessageBox.warning(
                self,
                "Invalid Member",
                "First name cannot be blank.",
            )
            self.first_name_input.setFocus()
            return

        if not last_name:
            QMessageBox.warning(
                self,
                "Invalid Member",
                "Last name cannot be blank.",
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

        member_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone or None,
        }

        self.save_requested.emit(member_data)

    def get_member_data(self):
        return {
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip() or None,
        }