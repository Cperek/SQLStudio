from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QStackedLayout, QVBoxLayout,QHBoxLayout, QWidget, QDesktopWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        with open('themes/MaterialDark.qss', 'r') as file:
            theme = file.read()

        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        button = QPushButton("Connect")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        layout.addWidget(self.text_input("Host"))
        layout.addWidget(self.text_input("User"))
        layout.addWidget(self.text_input("Password"))
        layout.addWidget(button)

        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0,0,0,0)
        
        self.mainView = QWidget()
        self.mainView.setLayout(layout)

        self.setStyleSheet(theme)
        self.setFixedSize(QSize(350, 200))
        self.setCentralWidget(self.mainView)
        

    def the_button_was_clicked(self):
        print("Connected!")
        self.setFixedSize(QSize(1250, 700))
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.mainView.deleteLater()


    def text_input(self, text : str):
        field = QHBoxLayout();
        input_ = QLineEdit();
        label = QLabel(text)

        input_.setFixedWidth(250)

        field.addWidget(label)
        field.addWidget(input_)
        widget = QWidget()
        widget.setLayout(field)
        return widget;


app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec()
