from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget
from mysql_connect import MySQLConnect
import sys, json
from inputs import Inputs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_connection()

    def initUI(self):
        self.setWindowTitle("SQL STUDIO")
        self.fields = {}
        self.setFixedSize(QSize(350, 200))
        
        with open('themes/ManjaroMix.qss', 'r') as file:
            theme = file.read()
        self.setStyleSheet(theme)

        layout = self.connectionForm()
        self.mainView = QWidget()
        self.mainView.setLayout(layout)
        self.setCentralWidget(self.mainView)

    def connectionForm(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(Inputs.text(self, "Host"))
        layout.addWidget(Inputs.text(self, "User"))
        layout.addWidget(Inputs.password(self, "Password"))
        layout.addWidget(Inputs.checkbox(self, "Save connection?"))
        layout.addSpacing(40)
        layout.addWidget(Inputs.button("Connect", self.submit_connection))

        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 30, 0, 0)
        return layout

    def databasesList(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        for record in self.connection.query:
            layout.addWidget(Inputs.button(record[0], self.selectDatabase))

        return layout

    def selectDatabase(self):
        print("Database selected")

    def submit_connection(self):
        self.setFixedSize(QSize(1250, 700))
        self.center()

        localhost = self.fields["Host"].text()
        user = self.fields["User"].text()
        password = self.fields["Password"].text()
        saveme = self.fields["Save connection?"]

        if saveme.isChecked():
            self.save_connection(localhost, user, password)
        else:
            self.save_connection("", "", "")

        self.connection = MySQLConnect(localhost, user, password)
        
        layout = self.databasesList()

        self.mainView = QWidget()
        self.mainView.setLayout(layout)
        self.mainView.setFixedSize(QSize(250, 700))
        self.setCentralWidget(self.mainView)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.mainView.deleteLater()

    def save_connection(self, host, user, password):
        with open('datas/connection.json', 'w') as file:
            json.dump({"host": host, "user": user, "password": password}, file)

    def load_connection(self):
        try:
            with open('datas/connection.json', 'r') as file:
                data = json.load(file)
                self.fields["Host"].setText(data["host"])
                self.fields["User"].setText(data["user"])
                self.fields["Password"].setText(data["password"])

                if data["host"] or data["user"] or data["password"]:
                    self.fields["Save connection?"].setChecked(True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading connection: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())