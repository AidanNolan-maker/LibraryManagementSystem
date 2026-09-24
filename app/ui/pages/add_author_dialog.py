from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

class AddAuthorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Author")
        self.setMinimumWidth(400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText(
            "Enter first name"
        )

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText(
            "Enter last name"
        )

        form_layout.addRow(
            "First Name:",
            self.first_name_input,
        )

        form_layout.addRow(
            "Last Name:",
            self.last_name_input,
        )

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

    def get_author_data(self):
        return {
            "first_name": self.first_name_input.text(),
            "last_name": self.last_name_input.text()
        }