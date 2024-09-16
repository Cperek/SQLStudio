from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from inputs import Inputs

class DatabaseList(QScrollArea):
    def __init__(self, connection, select_database_callback):
        super().__init__()
        self.connection = connection
        self.select_database_callback = select_database_callback
        self.databases = []

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.clear_spacing(layout)
        for record in connection.databases:
            button = Inputs.create_button(record[0], lambda checked, db=record[0]: self.select_database(db))
            self.databases.append(button)
            button.setFixedWidth(250)
            layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setFixedWidth(250)
        widget.setObjectName("databasesList")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(widget)

    def select_database(self, database):
        self.select_database_callback(database)

    def uncheck_all_except(self, database):
        for button in self.databases:
            if button.text() != database:
                button.setChecked(False)

    def clear_spacing(self, layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)