from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget, QHBoxLayout, QScrollArea, QTabWidget
from mysql_connect import MySQLConnect
import sys
import json
from inputs import Inputs
from database_list import DatabaseList
from tables_list import TablesList
from table_element import Table


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inputs = Inputs()
        self.initUI()
        self.load_connection()
        self.connection = None
        

    def initUI(self):
        self.setWindowTitle("CrunchSQL - Database Manager")
        self.setFixedSize(QSize(350, 200))
        self.set_theme()

        layout = self.create_connection_form()
        self.main_view = QWidget()
        self.main_view.setLayout(layout)
        self.setCentralWidget(self.main_view)

    def set_theme(self):
        try:
            with open('themes/ManjaroMix.qss', 'r') as file:
                theme = file.read()
            self.setStyleSheet(theme)
        except FileNotFoundError:
            print("Theme file not found. Using default theme.")

    def create_connection_form(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self.inputs.create_text_input("Host"))
        layout.addWidget(self.inputs.create_text_input("User"))
        layout.addWidget(self.inputs.create_password_input("Password"))
        layout.addWidget(self.inputs.create_checkbox("Save connection?"))
        layout.addSpacing(40)
        layout.addWidget(Inputs.create_button("Connect", self.submit_connection))
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 30, 0, 0)
        return layout

    def submit_connection(self):
        self.setMaximumSize(QSize(16777215, 16777215))
        self.setMinimumSize(QSize(1250,700))
        self.center()

        host = self.inputs.fields["Host"].text()
        user = self.inputs.fields["User"].text()
        password = self.inputs.fields["Password"].text()
        save_connection = self.inputs.fields["Save connection?"]

        if save_connection.isChecked():
            self.save_connection(host, user, password)
        else:
            self.save_connection("", "", "")

        try:
            self.connection = MySQLConnect(host, user, password)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return

        self.setup_tabs()

    def setup_tabs(self):
        self.left_tab_bar = QTabWidget()
        self.left_tab_bar.setTabPosition(QTabWidget.West)

        self.database_list = DatabaseList(self.connection, self.select_database)
        self.left_tab_bar.addTab(self.database_list, "Databases")

        self.tables_list = TablesList(self.connection, self.select_table)
        self.left_tab_bar.addTab(self.tables_list, "Tables")

        self.general_layout = QHBoxLayout()
        self.general_layout.addWidget(self.left_tab_bar, alignment=Qt.AlignLeft)

        self.clear_spacing(self.general_layout)
        self.general_layout.setAlignment(Qt.AlignTop)

        widget = QWidget()
        widget.setLayout(self.general_layout)
        self.setCentralWidget(widget)

    def select_database(self, database):
        self.database_list.uncheck_all_except(database)
        self.tables_list.update_tables(database)
        self.left_tab_bar.setCurrentIndex(1)

    def select_table(self, table):
        self.tables_list.uncheck_all_except(table)

        if hasattr(self, 'tableElemet'):
            self.general_layout.removeWidget(self.tableElemet)
            self.tableElemet.deleteLater()

        self.tableElemet = Table(self.connection, table)
        self.general_layout.addWidget(self.tableElemet)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.main_view.deleteLater()

    def save_connection(self, host: str, user: str, password: str):
        with open('datas/connection.json', 'w') as file:
            json.dump({"host": host, "user": user, "password": password}, file)

    def load_connection(self):
        try:
            with open('datas/connection.json', 'r') as file:
                data = json.load(file)
                self.inputs.fields["Host"].setText(data["host"])
                self.inputs.fields["User"].setText(data["user"])
                self.inputs.fields["Password"].setText(data["password"])

                if data["host"] or data["user"] or data["password"]:
                    self.inputs.fields["Save connection?"].setChecked(True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading connection: {e}")

    def clear_spacing(self, layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())