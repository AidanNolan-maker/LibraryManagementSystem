from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.ui.styles import APPLICATION_STYLE

from app.ui.pages.books_page import BooksPage
from app.ui.pages.authors_page import AuthorsPage
from app.ui.pages.members_page import MembersPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.resize(1200, 800)

        self.setStyleSheet(APPLICATION_STYLE)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        content_area = QWidget()
        content_area.setObjectName("content_area")

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(30, 30, 30, 30)

        self.pages = QStackedWidget()
        content_layout.addWidget(self.pages) 

        main_layout.addWidget(content_area)

        self.create_pages()

        self.show_page(0)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        title = QLabel("Library\nManagement")
        title.setObjectName("sidebar_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(20)

        self.dashboard_button = self.create_nav_button("Dashboard")
        self.books_button = self.create_nav_button("Books")
        self.authors_button = self.create_nav_button("Authors")
        self.members_button = self.create_nav_button("Members")
        self.loans_button = self.create_nav_button("Loans")
        self.reports_button = self.create_nav_button("Reports")

        sidebar_layout.addWidget(self.dashboard_button)
        sidebar_layout.addWidget(self.books_button)
        sidebar_layout.addWidget(self.authors_button)
        sidebar_layout.addWidget(self.members_button)
        sidebar_layout.addWidget(self.loans_button)
        sidebar_layout.addWidget(self.reports_button)

        sidebar_layout.addStretch()

        self.dashboard_button.clicked.connect(
            lambda: self.show_page(0)
        )
        self.books_button.clicked.connect(
            lambda: self.show_page(1)
        )
        self.authors_button.clicked.connect(
            lambda: self.show_page(2)
        )
        self.members_button.clicked.connect(
            lambda: self.show_page(3)
        )
        self.loans_button.clicked.connect(
            lambda: self.show_page(4)
        )
        self.reports_button.clicked.connect(
            lambda: self.show_page(5)
        )

        return sidebar

    @staticmethod
    def create_nav_button(text):
        button = QPushButton(text)
        button.setObjectName("nav_button")
        button.setMinimumHeight(45)
        button.setCheckable(True)

        return button

    def create_pages(self):
        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)

        dashboard_title = QLabel("Dashboard")
        dashboard_title.setObjectName("page_title")

        dashboard_layout.addWidget(dashboard_title)
        dashboard_layout.addStretch()

        self.pages.addWidget(dashboard_page)

        self.pages.addWidget(BooksPage())
        self.pages.addWidget(AuthorsPage())
        self.pages.addWidget(MembersPage())

        for page_name in ["Loans", "Reports"]:
            page = QWidget()

            layout = QVBoxLayout(page)

            title = QLabel(page_name)
            title.setObjectName("page_title")

            layout.addWidget(title)
            layout.addStretch()

            self.pages.addWidget(page)

    def show_page(self, index):
        self.pages.setCurrentIndex(index)

        buttons = [
            self.dashboard_button,
            self.books_button,
            self.authors_button,
            self.members_button,
            self.loans_button,
            self.reports_button,
        ]

        for button_index, button in enumerate(buttons):
            button.setChecked(button_index == index)