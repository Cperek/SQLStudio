from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QStackedLayout, QVBoxLayout,QHBoxLayout, QWidget, QDesktopWidget, QCheckBox
from mysql_connect import MySQLConnect
import sys, json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        with open('themes/ManjaroMix.qss', 'r') as file:
            theme = file.read()

        self.setWindowTitle("SQL STUDIO")
        self.fields = {}

        layout = QVBoxLayout()

        button = QPushButton("Connect")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        layout.addWidget(self.text_input("Host"))
        layout.addWidget(self.text_input("User"))
        layout.addWidget(self.text_input("Password"))
        layout.addWidget(self.checkbox_input("Save conncetion?"))
        layout.addSpacing(40)
        layout.addWidget(button)

        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,30,0,0)
        
        self.mainView = QWidget()
        self.mainView.setLayout(layout)

        self.setStyleSheet(theme)
        self.setFixedSize(QSize(350, 200))
        self.setCentralWidget(self.mainView)
        self.load_connection()
        #self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowFlag(Qt.FramelessWindowHint)
        #self.mainView.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")
        

    def the_button_was_clicked(self):
        print("Connected!")
        self.setFixedSize(QSize(1250, 700))
        self.center()
        localhost = self.fields["Host"].text();
        user = self.fields["User"].text();
        password = self.fields["Password"].text();
        saveme = self.fields["Save conncetion?"];
        
        if(saveme.isChecked()):
            self.save_connection(localhost, user, password)
        else:
            self.save_connection("", "", "")

        self.connection = MySQLConnect(localhost, user, password)
        layout = QVBoxLayout();
        for record in self.connection.query:
            label = QPushButton(record[0])
            layout.addWidget(label)
        
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
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


    def text_input(self, text : str):
        field = QHBoxLayout();
        input_ = QLineEdit();
        input_.setFixedWidth(250)

        self.fields[text] = input_

        label = QLabel(text)

        field.addWidget(label)
        field.addWidget(input_)
        field.setAlignment(Qt.AlignCenter)
        field.setContentsMargins(10,0,10,5)
        widget = QWidget()
        widget.setLayout(field)
        return widget;
        
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

                if(data["host"] != "" or data["user"] != "" or data["password"] != ""):
                    self.fields["Save conncetion?"].setChecked(True)
        except NameError:
            print(NameError)
            return

    def checkbox_input(self, text : str):
        field = QHBoxLayout();
        input_ = QCheckBox();
        self.fields[text] = input_

        label = QLabel(text)

        field.addWidget(input_)
        field.addWidget(label)
        field.setAlignment(Qt.AlignLeft)
        field.setContentsMargins(10,0,10,5)
        widget = QWidget()
        widget.setLayout(field)
        return widget;

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()
