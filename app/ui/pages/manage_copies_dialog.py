from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from app.database.models import Book
from app.database.database import SessionLocal
from app.services.book_copy_service import BookCopyService

class ManageCopiesDialog(QDialog):
    def __init__(self, book: Book, parent=None):
        super().__init__(parent)

        self.book = book

        self.setWindowTitle(f"Manage Copies - {book.title}")
        self.setMinimumSize(500, 400)

        self.setup_ui()
        self.load_copies()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel(f"Copies of: {self.book.title}")
        title_label.setObjectName("page_title")

        self.copy_table = QTableWidget()
        self.copy_table.setColumnCount(2)
        self.copy_table.setHorizontalHeaderLabels(
            ["Copy ID", "Status"]
        )
        self.copy_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.copy_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.copy_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.copy_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.add_copy_button = QPushButton("Add Copy")
        self.add_copy_button.clicked.connect(self.add_copy)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )
        button_box.rejected.connect(self.reject)

        layout.addWidget(title_label)
        layout.addWidget(self.copy_table)
        layout.addWidget(self.add_copy_button)
        layout.addWidget(button_box)

    def load_copies(self):
        db = SessionLocal()

        try:
            service = BookCopyService(db)
            copies = service.get_copies_for_book(self.book.id)

            self.copy_table.setRowCount(len(copies))

            for row, copy in enumerate(copies):
                self.copy_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(str(copy.id)),
                )
                self.copy_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(copy.status),
                )

        finally:
            db.close()

    def add_copy(self):
        confirmation = QMessageBox.question(
            self,
            "Add Copy",
            f'Add a new physical copy of "{self.book.title}"?',
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        db = SessionLocal()

        try:
            service = BookCopyService(db)
            service.create_copy(self.book.id)
            self.load_copies()

        finally:
            db.close()