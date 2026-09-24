from app.database.models import Author, Book
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

class EditBookDialog(QDialog):
    def __init__(
            self,
            book: Book,
            authors: list[Author],
            parent=None,
    ):
        super().__init__(parent)

        self.book = book

        self.setWindowTitle("Edit Book")
        self.setMinimumWidth(400)

        self.setup_ui()
        self.set_authors(authors)
        self.populate_fields()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.title_input = QLineEdit()

        self.isbn_input = QLineEdit()

        self.publication_year_input = QSpinBox()
        self.publication_year_input.setRange(0, 9999)
        self.publication_year_input.setSpecialValueText(
            "Not specified"
        )

        self.genre_input = QLineEdit()

        self.author_input = QComboBox()

        form_layout.addRow(
            "Title:",
            self.title_input,
        )

        form_layout.addRow(
            "ISBN:",
            self.isbn_input,
        )

        form_layout.addRow(
            "Publication Year:",
            self.publication_year_input,
        )

        form_layout.addRow(
            "Genre",
            self.genre_input,
        )

        form_layout.addRow(
            "Author:",
            self.author_input,
        )

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
            display_name = (
                f"{author.first_name} {author.last_name}"
            )

            self.author_input.addItem(
                display_name,
                userData=author.id,
            )

    def populate_fields(self):
        self.title_input.setText(self.book.title)
        self.isbn_input.setText(self.book.isbn)

        if self.book.publication_year is not None:
            self.publication_year_input.setValue(
                self.book.publication_year
            )
        else:
            self.publication_year_input.setValue(0)

        if self.book.genre is not None:
            self.genre_input.setText(self.book.genre)

        author_index = self.author_input.findData(
            self.book.author_id
        )

        if author_index >= 0:
            self.author_input.setCurrentIndex(
                author_index
            )

    def get_book_data(self):
        publication_year = (
            self.publication_year_input.value()
        )

        if publication_year == 0:
            publication_year = None

        return {
            "title": self.title_input.text(),
            "isbn": self.isbn_input.text(),
            "publication_year": publication_year,
            "genre": self.genre_input.text(),
            "author_id": self.author_input.currentData(),
        }