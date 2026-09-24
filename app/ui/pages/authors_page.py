from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QDialog,
    QPushButton,
    QMessageBox,
)

from app.database.database import SessionLocal
from app.services.author_service import AuthorService
from app.ui.pages.add_author_dialog import AddAuthorDialog

class AuthorsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.load_authors()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel("Authors")
        title_label.setObjectName("page_title")

        self.add_author_button = QPushButton("Add Author")
        self.add_author_button.clicked.connect(
            self.open_add_author_dialog
        )

        self.author_table = QTableWidget()
        self.author_table.setColumnCount(3)
        self.author_table.setHorizontalHeaderLabels(
            [
                "ID",
                "First Name",
                "Last Name",
            ]
        )

        self.author_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.author_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.author_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(title_label)
        layout.addWidget(self.add_author_button)
        layout.addWidget(self.author_table)

    def load_authors(self):
        db = SessionLocal()

        try:
            service = AuthorService(db)
            authors = service.get_all_authors()

            self.populate_table(authors)

        finally:
            db.close()

    def populate_table(self, authors):
        self.author_table.setRowCount(len(authors))

        for row, author in enumerate(authors):
            self.author_table.setItem(
                row,
                0,
                QTableWidgetItem(str(author.id)),
            )

            self.author_table.setItem(
                row,
                1,
                QTableWidgetItem(author.first_name),
            )

            self.author_table.setItem(
                row,
                2,
                QTableWidgetItem(author.last_name),
            )

    def open_add_author_dialog(self):
        dialog = AddAuthorDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        author_data = dialog.get_author_data()

        db = SessionLocal()

        try:
            service = AuthorService(db)

            service.create_author(
                first_name=author_data["first_name"],
                last_name=author_data["last_name"],
            )

            self.load_authors()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to Add Author",
                str(error)
            )

        finally:
            db.close()