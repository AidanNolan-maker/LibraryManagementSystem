from PySide6.QtWidgets import (
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
)

from app.database.database import SessionLocal
from app.services.member_service import MemberService
from app.ui.pages.add_member_dialog import AddMemberDialog
from app.ui.pages.edit_member_dialog import EditMemberDialog

class MembersPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_members()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Members")
        title.setObjectName("page_title")

        button_layout = QHBoxLayout()

        self.add_member_button = QPushButton("Add Member")
        self.add_member_button.clicked.connect(self.open_add_member_dialog)

        self.edit_member_button = QPushButton("Edit Member")
        self.edit_member_button.clicked.connect(self.edit_selected_member)

        self.archive_member_button = QPushButton("Archive Member")
        self.archive_member_button.clicked.connect(self.archive_selected_member)

        button_layout.addWidget(self.add_member_button)
        button_layout.addWidget(self.edit_member_button)
        button_layout.addWidget(self.archive_member_button)
        button_layout.addStretch()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search members by name, email, or phone..."
        )
        self.search_input.textChanged.connect(self.search_members)

        self.member_table = QTableWidget()
        self.member_table.setColumnCount(6)
        self.member_table.setHorizontalHeaderLabels(
            [
                "ID",
                "First Name",
                "Last Name",
                "Email",
                "Phone",
                "Membership Date",
            ]
        )

        self.member_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.member_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.member_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        header = self.member_table.horizontalHeader()

        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(title)
        layout.addLayout(button_layout)
        layout.addWidget(self.search_input)
        layout.addWidget(self.member_table)

    def load_members(self, search_term=""):
        db = SessionLocal()

        try:
            service = MemberService(db)

            if search_term.strip():
                members = service.search_members(search_term.strip())

            else:
                members = service.get_all_members()

            self.member_table.setRowCount(len(members))

            for row, member in enumerate(members):
                self.member_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(str(member.id)),
                )
                self.member_table.setItem(
                    row,
                    1,
                    QTableWidgetItem(member.first_name),
                )
                self.member_table.setItem(
                    row,
                    2,
                    QTableWidgetItem(member.last_name),
                )
                self.member_table.setItem(
                    row,
                    3,
                    QTableWidgetItem(member.email),
                )
                self.member_table.setItem(
                    row,
                    4,
                    QTableWidgetItem(member.phone or ""),
                )
                self.member_table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        member.membership_date.strftime("%Y-%m-%d")
                    ),
                )

        finally:
            db.close()

    def search_members(self):
        self.load_members(self.search_input.text())

    def open_add_member_dialog(self):
        dialog = AddMemberDialog(self)

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        member_data = dialog.get_member_data()


        db = SessionLocal()

        try:
            service = MemberService(db)

            service.create_member(
                first_name=member_data["first_name"],
                last_name=member_data["last_name"],
                email=member_data["email"],
                phone=member_data["phone"],
            )

            self.load_members()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to Add Member",
                str(error)
            )

        finally:
            db.close()

    def archive_selected_member(self):
        selected_rows = self.member_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Member Selected",
                "Please select a member to archive.",
            )
            return

        row = selected_rows[0].row()
        member_id_item = self.member_table.item(row, 0)

        if member_id_item is None:
            QMessageBox.warning(
                self,
                "Invalid Selection",
                "The selected member does not have a valid ID.",
            )
            return

        member_id = int(member_id_item.text())

        db = SessionLocal()

        try:
            service = MemberService(db)
            member = service.get_member_by_id(member_id)

            if member is None:
                QMessageBox.warning(
                    self,
                    "Member Not Found",
                    "The selected member could not be found.",
                )
                return

            confirmation = QMessageBox.question(
                self,
                "Archive Member",
                (
                    f'Are you sure you want to archive '
                    f'"{member.first_name} {member.last_name}"?'
                ),
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if confirmation != QMessageBox.StandardButton.Yes:
                return

            service.archive_member(member)

            self.load_members()

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to Archive Member",
                str(error),
            )

        finally:
            db.close()

    def edit_selected_member(self):
        selected_rows = self.member_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(
                self,
                "No Member Selected",
                "Please select a member to edit.",
            )
            return

        row = selected_rows[0].row()

        member_id_item = self.member_table.item(row, 0)

        if member_id_item is None:
            QMessageBox.warning(
                self,
                "Invalid Selection",
                "The selected member does not have a valid ID.",
            )
            return

        member_id = int(member_id_item.text())

        db = SessionLocal()

        try:
            service = MemberService(db)

            member = service.get_member_by_id(member_id)

            if member is None:
                QMessageBox.warning(
                    self,
                    "Member Not Found",
                    "The selected member could not be found.",
                )
                return

            dialog = EditMemberDialog(member, self)

            def save_member(member_data):
                member.first_name = member_data["first_name"]
                member.last_name = member_data["last_name"]
                member.email = member_data["email"]
                member.phone = member_data["phone"]

                try:
                    service.update_member(member)

                except ValueError as error:
                    QMessageBox.warning(
                        dialog,
                        "Unable to Edit Member",
                        str(error),
                    )
                    return

                dialog.accept()

            dialog.save_requested.connect(save_member)

            if dialog.exec() == dialog.DialogCode.Accepted:
                self.load_members()

        finally:
            db.close()
