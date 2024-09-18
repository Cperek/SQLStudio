from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class Table(QWidget):
    def __init__(self, connection, table):
        super().__init__()
        self.connection = connection
        self.headers = {}
        self.order = Qt.AscendingOrder
        self.vbox = QVBoxLayout()
        self.clear_spacing(self.vbox)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.table = QTableWidget()  
        self.table.setObjectName("table_preview")
        self.scroll.setWidget(self.table)

        self.setup_ui()

        columns = connection.show_columns(table)
        records = connection.select_all(table)
        self.table.setRowCount(len(records))
        self.table.setColumnCount(len(columns))

        for column in columns:
            header = QTableWidgetItem(column[0])
            header.setIcon(QIcon("icons/sort-solid.svg"))
            header.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.headers[columns.index(column)] = header
            self.table.setHorizontalHeaderItem(columns.index(column),header)

        for record in records:
            for column in columns:
                item = QTableWidgetItem(str(record[columns.index(column)]))
                #item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(records.index(record), columns.index(column), item)

        #self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self.sort)

        self.clear_spacing(self.vbox)
        self.scroll.setMinimumHeight(700)
        self.scroll.setObjectName("tableElement")

    def sort(self, column):
        self.table.sortItems(column, self.order)

        if self.order == Qt.AscendingOrder:

            self.order = Qt.DescendingOrder
            self.headers[column].setIcon(QIcon("icons/sort-up-solid.svg"))
        else:
            self.order = Qt.AscendingOrder
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
