from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

class Table(QWidget):
    def __init__(self, connection, table):
        super().__init__()
        self.connection = connection

        self.vbox = QVBoxLayout()
        self.clear_spacing(self.vbox)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.table = QTableWidget()  
        self.scroll.setWidget(self.table)

        self.setup_ui()

        columns = connection.show_columns(table)
        records = connection.select_all(table)
        self.table.setRowCount(len(records) + 1)
        self.table.setColumnCount(len(columns))

        for column in columns:
            self.table.setItem(0, columns.index(column), QTableWidgetItem(column[0]))

        for record in records:
            for column in columns:
                item = QTableWidgetItem(str(record[columns.index(column)]))
                #item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(records.index(record)+1, columns.index(column), item)

        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.clear_spacing(self.vbox)
        self.scroll.setMinimumHeight(700)
        self.scroll.setObjectName("tableElement")

    def setup_ui(self):
        layout = QVBoxLayout()
        self.clear_spacing(layout)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def clear_spacing(self, layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
