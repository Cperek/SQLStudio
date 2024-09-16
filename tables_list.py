from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from inputs import Inputs

class TablesList(QWidget):
    def __init__(self, connection, select_table_callback):
        super().__init__()
        self.connection = connection
        self.select_table_callback = select_table_callback
        self.tables = []

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(Qt.AlignTop)

        self.scroll = QScrollArea()
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(QWidget())

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def update_tables(self, database):
        for table in self.tables:
            table.deleteLater()

        self.tables = []
        self.connection.use_database(database)

        for table in self.connection.fetch_tables():
            button = Inputs.create_button(table[0], lambda checked, table=table[0]: self.select_table(table))
            button.setFixedWidth(250)
            self.vbox.addWidget(button)
            self.tables.append(button)

        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(Qt.AlignTop)
        self.scroll.widget().setLayout(self.vbox)
        self.scroll.setFixedSize(250, 700)
        self.scroll.widget().setObjectName("tablesList")

    def select_table(self, table):
        self.select_table_callback(table)

    def uncheck_all_except(self, table):
        for button in self.tables:
            if button.text() != table:
                button.setChecked(False)