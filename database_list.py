from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from inputs import Inputs

class DatabaseList(QWidget):
    def __init__(self, connection, select_database_callback):
        super().__init__()
        self.connection = connection
        self.select_database_callback = select_database_callback
        self.databases = []

        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(QWidget())

        self.setup_ui()
        
        for record in connection.databases:
            button = Inputs.create_button(record[0], lambda checked, db=record[0]: self.select_database(db))
            self.databases.append(button)
            button.setFixedWidth(250)
            self.vbox.addWidget(button)

        self.scroll.widget().setLayout(self.vbox)
        self.scroll.setFixedWidth(250);
        self.scroll.setMinimumHeight(700);
        self.scroll.widget().setObjectName("databasesList")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.search_input = Inputs.create_search_input('Search...', lambda text: self.search(text))
        layout.addWidget(self.search_input)  
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def search(self, text):
        for db in self.databases:
            if text.lower() in db.text().lower():
                db.show()
            else:
                db.hide()

    def select_database(self, database):
        self.select_database_callback(database)

    def uncheck_all_except(self, database):
        for button in self.databases:
            if button.text() != database:
                button.setChecked(False)

    def clear_spacing(self, layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
