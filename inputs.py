from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLineEdit, QLabel, QWidget, QCheckBox, QPushButton
from PyQt5.QtCore import Qt

class Inputs:
    def __init__(self):
        self.fields = {}

    def create_text_input(self, label_text: str) -> QWidget:
        input_field = QLineEdit()
        input_field.setFixedWidth(250)
        label = QLabel(label_text)
        self.fields[label_text] = input_field
        return self._build_widget(input_field, label, Qt.AlignCenter)
    
    def create_password_input(self, label_text: str) -> QWidget:
        input_field = QLineEdit()
        input_field.setFixedWidth(250)
        input_field.setEchoMode(QLineEdit.Password)
        label = QLabel(label_text)
        self.fields[label_text] = input_field
        return self._build_widget(input_field, label, Qt.AlignCenter)

    def create_checkbox(self, label_text: str) -> QWidget:
        checkbox = QCheckBox()
        label = QLabel(label_text)
        self.fields[label_text] = checkbox
        return self._build_widget(checkbox, label, Qt.AlignLeft, 'right')

    @staticmethod
    def create_button(label_text: str, action=None) -> QPushButton:
        button = QPushButton(label_text)
        button.setCheckable(True)
        if action:
            button.clicked.connect(action)
        return button

    @staticmethod
    def create_search_input(label_text: str, action=None) -> QLineEdit:
        input_field = QLineEdit()
        input_field.setFixedWidth(250)
        input_field.setPlaceholderText(label_text)
        if action:
            input_field.textChanged.connect(action)

        return input_field

    def _build_widget(self, input_field, label, alignment, label_placement='left') -> QWidget:
        layout = QHBoxLayout()
        if label_placement == 'left':
            layout.addWidget(label)
            layout.addWidget(input_field)
        else:
            layout.addWidget(input_field)
            layout.addWidget(label)
        layout.setAlignment(alignment)
        layout.setContentsMargins(10, 0, 10, 5)
        widget = QWidget()
        widget.setLayout(layout)
        return widget