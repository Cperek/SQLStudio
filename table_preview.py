from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Table(QWidget):
    def __init__(self, connection, table):
        super().__init__()
        self.connection = connection
        self.table_name = table
        self.headers = {}
        self.order = 'ASC'
        self.vbox = QVBoxLayout()
        self.clear_spacing(self.vbox)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.table = QTableWidget()  
        self.table.setObjectName("table_preview")
        #self.table.setSortingEnabled(True)
        self.scroll.setWidget(self.table)

        self.setup_ui()

        self.columns = connection.show_columns(table)
        records = connection.select_all(table)
        self.table.setRowCount(len(records))
        self.table.setColumnCount(len(self.columns))

        for column in self.columns:
            header = QTableWidgetItem(column[0])
            header.setIcon(QIcon("icons/sort-solid.svg"))
            header.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.headers[self.columns.index(column)] = header
            self.table.setHorizontalHeaderItem(self.columns.index(column),header)

        self.buildRows(records)

        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self.sort)

        self.clear_spacing(self.vbox)
        self.scroll.setMinimumHeight(700)
        self.scroll.setObjectName("tableElement")

    def buildRows(self, records):
        for record in records:
            for column in self.columns:
                item = QTableWidgetItem(str(record[self.columns.index(column)]))
                self.table.setItem(records.index(record), self.columns.index(column), item)

    def sort(self, column):
        #slow but had issues with build-in QTableWidget SortItems...
        records = self.connection.select_all(self.table_name,self.headers[column].text(), self.order)
        self.table.setRowCount(len(records))
        self.buildRows(records)

        if self.order == 'ASC':

            self.order = 'DESC'
            self.headers[column].setIcon(QIcon("icons/sort-up-solid.svg"))
        else:
            self.order = 'ASC'
            self.headers[column].setIcon(QIcon("icons/sort-down-solid.svg"))

        for key in self.headers:
            if key != column:
                self.headers[key].setIcon(QIcon("icons/sort-solid.svg"))

    def setup_ui(self):
        layout = QVBoxLayout()
        self.clear_spacing(layout)
        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def clear_spacing(self, layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignLeft)
