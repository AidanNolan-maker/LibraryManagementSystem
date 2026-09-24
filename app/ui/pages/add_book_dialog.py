from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

from app.database.models import Author

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add Book")
        self.setMinimumWidth(400)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter book title")

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("Enter ISBN")

        self.publication_year_input = QSpinBox()
        self.publication_year_input.setRange(0, 9999)
        self.publication_year_input.setSpecialValueText("Not specified")

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Enter genre")

        self.author_input = QComboBox()

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        form_layout.addRow(
            "Publication Year:",
            self.publication_year_input,
        )
        form_layout.addRow("Genre:", self.genre_input)
        form_layout.addRow("Author:", self.author_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(button_box)

    def set_authors(self, authors: list[Author]):
        self.author_input.clear()

        for author in authors:
            display_name = f"{author.first_name} {author.last_name}"

            self.author_input.addItem(
                display_name,
                userData=author.id,
            )

    def get_book_data(self):
        publication_year = self.publication_year_input.value()

        if publication_year == 0:
            publication_year = None

        return {
            "title": self.title_input.text(),
            "isbn": self.isbn_input.text(),
            "publication_year": publication_year,
            "genre": self.genre_input.text(),
            "author_id": self.author_input.currentData(),
        }