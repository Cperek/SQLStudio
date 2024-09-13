from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget,QHBoxLayout, QScrollArea, QTabWidget
from mysql_connect import MySQLConnect
import sys, json
from inputs import Inputs

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inputs = Inputs()
        self.initUI()
        self.load_connection()

    def initUI(self):
        self.setWindowTitle("CrunchSQL - Database Manager")
        self.setFixedSize(QSize(350, 200))
        
        try:
            with open('themes/ManjaroMix.qss', 'r') as file:
                theme = file.read()
            self.setStyleSheet(theme)
        except FileNotFoundError:
            print("Theme file not found. Using default theme.")

        layout = self.connectionForm()
        self.mainView = QWidget()
        self.mainView.setLayout(layout)
        self.setCentralWidget(self.mainView)

    def connectionForm(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(self.inputs.text("Host"))
        layout.addWidget(self.inputs.text("User"))
        layout.addWidget(self.inputs.password("Password"))
        layout.addWidget(self.inputs.checkbox("Save connection?"))
        layout.addSpacing(40)
        layout.addWidget(Inputs.button("Connect", self.submit_connection))
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 30, 0, 0)
        return layout

    def databasesList(self) -> QWidget:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.databases = []
        self.clearSpacing(layout)
        for record in self.connection.query:
            button = Inputs.button(record[0], lambda checked, db=record[0]: self.selectDatabase(db))
            self.databases.append(button)
            button.setFixedWidth(250)
            layout.addWidget(button)

        widget = QWidget()
        widget.setObjectName("databasesList")
        widget.setLayout(layout)
        widget.setFixedSize(QSize(250, 700))
        return widget

    def selectDatabase(self,database):
        print(database)
        print(self.vbox.count())

        for db in self.databases:
            db.setChecked(False)
            if(db.text() == database):
                db.setChecked(True)
            

        for i in reversed(range(self.vbox.count())): 
            self.vbox.itemAt(i).widget().deleteLater()

        self.connection.use_database(database)
        self.tables = []
        for table in self.connection.fetch_tables():
            button = self.inputs.button(table[0], lambda checked, table=table[0]: self.selectTable(table))
            self.tables.append(button)
            button.setFixedWidth(250)
            self.vbox.addWidget(button)
        self.leftTabBar.setCurrentIndex(1)

    def selectTable(self,table):
        print(table)
        for table_ in self.tables:
            table_.setChecked(False)
            if(table_.text() == table):
                table_.setChecked(True)

    def submit_connection(self):
        self.setFixedSize(QSize(1250, 700))
        self.center()

        localhost = self.inputs.fields["Host"].text()
        user = self.inputs.fields["User"].text()
        password = self.inputs.fields["Password"].text()
        saveme = self.inputs.fields["Save connection?"]

        if saveme.isChecked():
            self.save_connection(localhost, user, password)
        else:
            self.save_connection("", "", "")

        try:
            self.connection = MySQLConnect(localhost, user, password)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout() 
        self.vbox.setAlignment(Qt.AlignTop)
        self.clearSpacing(self.vbox)              # The Vertical Box that contains the Horizontal Boxes of  labels and buttons



        self.widget.setLayout(self.vbox)
        self.widget.setFixedWidth(250)
        self.widget.setObjectName("tablesList")
        #Scroll Area Properties
        #self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        

        self.fixed = QWidget()
        self.fixed.adjustSize()

        self.dbList = self.databasesList()

        self.leftTabBar = QTabWidget()
        self.leftTabBar.setTabPosition(QTabWidget.West)

        self.leftTabBar.addTab(self.dbList,"Databases")
        self.leftTabBar.addTab(self.scroll,"Tables")
        self.leftTabBar.setStyleSheet("""
            QTabBar::tab {
                width: 30px;   /* Adjust width */
                padding: 5px;
                border-bottom: 1px solid black;
            }
            QTabWidget::tab-bar {
                alignment: left;  /* Align text to the top */
            }
        """)

        
        general = self.buildLayout(
            layout  = QHBoxLayout(), 
            widgets = [
                self.leftTabBar,
                self.fixed

            ]
        )
        self.clearSpacing(general)
        general.setAlignment(Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(general)

        self.setCentralWidget(widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.mainView.deleteLater()

    def save_connection(self, host: str, user: str, password: str):
        with open('datas/connection.json', 'w') as file:
            json.dump({"host": host, "user": user, "password": password}, file)

    def clearSpacing(self,layout):
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def buildLayout(self, layout, widgets: list):
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def load_connection(self):
        try:
            with open('datas/connection.json', 'r') as file:
                data = json.load(file)
                self.inputs.fields["Host"].setText(data["host"])
                self.inputs.fields["User"].setText(data["user"])
                self.inputs.fields["Password"].setText(data["password"])

                if data["host"] or data["user"] or data["password"]:
                    self.inputs.fields["Save connection?"].setChecked(True)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading connection: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())