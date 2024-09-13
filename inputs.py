from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLineEdit, QLabel, QWidget, QCheckBox, QPushButton
from PyQt5.QtCore import Qt

class Inputs:
    def __init__(self):
        self.fields = {}

    def text(self, text: str) -> QWidget:
        input_ = QLineEdit()
        input_.setFixedWidth(250)
        label = QLabel(text)
        self.fields[text] = input_
        return buildWidget(input_, label, Qt.AlignCenter)

    def password(self, text: str) -> QWidget:
        input_ = QLineEdit()
        input_.setFixedWidth(250)
        input_.setEchoMode(QLineEdit.Password)
        label = QLabel(text)
        self.fields[text] = input_
        return buildWidget(input_, label, Qt.AlignCenter)

    def checkbox(self, text: str) -> QWidget:
        input_ = QCheckBox()
        label = QLabel(text)
        self.fields[text] = input_
        return buildWidget(input_, label, Qt.AlignLeft, 'right')

    @staticmethod
    def button(text: str, action = None) -> QPushButton:
        button = QPushButton(text)
        button.setCheckable(True)
        if action:
            button.clicked.connect(action)
        return button

def buildWidget(input_, label, align, label_placement='left') -> QWidget:
    field = QHBoxLayout()
    if label_placement == 'left':
        field.addWidget(label)
        field.addWidget(input_)
    else:
        field.addWidget(input_)
        field.addWidget(label)
    field.setAlignment(align)
    field.setContentsMargins(10, 0, 10, 5)
    widget = QWidget()
    widget.setLayout(field)
    return widget