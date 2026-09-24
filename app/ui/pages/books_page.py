from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QDialog,
    QMessageBox,
)

from app.database.database import SessionLocal
from app.services.book_service import BookService

from app.services.author_service import AuthorService
from app.ui.pages.add_book_dialog import AddBookDialog

class BooksPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.load_books()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel("Books")
        title_label.setObjectName("page_title")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books...")

        self.add_book_button = QPushButton("Add Book")
        self.add_book_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.book_table = QTableWidget()
        self.book_table.setColumnCount(5)
        self.book_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Title",
                "ISBN",
                "Publication Year",
                "Genre"
            ]
        )

        self.book_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.book_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.book_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.book_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.search_input.textChanged.connect(self.search_books)

        layout.addWidget(title_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.add_book_button)
        layout.addWidget(self.book_table)

    def load_books(self):
        db = SessionLocal()

        try:
            service = BookService(db)
            books = service.get_all_books()
            self.populate_table(books)

        finally:
            db.close()

    def search_books(self, search_term: str):
        db = SessionLocal()

        try:
            service = BookService(db)

            if search_term.strip():
                books = service.search_books(search_term.strip())
            else:
                books = service.get_all_books()

            self.populate_table(books)

        finally:
            db.close()

    def populate_table(self, books):
        self.book_table.setRowCount(len(books))

        for row, book in enumerate(books):
            self.book_table.setItem(
                row,
                0,
                QTableWidgetItem(str(book.id)),
            )

            self.book_table.setItem(
                row,
                1,
                QTableWidgetItem(book.title),
            )

            self.book_table.setItem(
                row,
                2,
                QTableWidgetItem(book.isbn),
            )

            publication_year = (
                str(book.publication_year)
                if book.publication_year is not None
                else ""
            )

            self.book_table.setItem(
                row,
                3,
                QTableWidgetItem(publication_year),
            )

            genre = book.genre if book.genre is not None else ""

            self.book_table.setItem(
                row,
                4,
                QTableWidgetItem(genre),
            )

    def open_add_book_dialog(self):
        db = SessionLocal()

        try:
            author_service = AuthorService(db)
            authors = author_service.get_all_authors()

            dialog = AddBookDialog(self)
            dialog.set_authors(authors)

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            book_data = dialog.get_book_data()

            book_service = BookService(db)

            try:
                book_service.create_book(
                    title=book_data["title"],
                    isbn=book_data["isbn"],
                    publication_year=book_data["publication_year"],
                    genre=book_data["genre"],
                    author_id=book_data["author_id"],
                )

            except ValueError as error:
                QMessageBox.warning(
                    self,
                    "Unable to Add Book",
                    str(error)
                )
                return

            self.load_books()

        finally:
            db.close()