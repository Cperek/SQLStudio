import mysql.connector
from mysql.connector import Error

class MySQLConnect:
    def __init__(self, host: str, user: str, password: str):
        globals()['query'] = []
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.databases = self._fetch_databases("SHOW DATABASES")
            self.log("SHOW DATABASES")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.databases = []

    def use_database(self, database: str):
        cursor = self.connection.cursor()
        sql = f"USE {database}"
        cursor.execute(sql)
        self.log(sql)
        cursor.close()

    def _fetch_databases(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        databases = cursor.fetchall()
        cursor.close()
        return databases
    
    def select_all(self, table: str, where: str = '', order_by: str = '', sort:str = 'ASC' ) -> list:
        cursor = self.connection.cursor()
        
        where = f"WHERE {where}" if where else ''

        sql = f"SELECT * FROM {table} {where}"
        if order_by:
            sql += f" ORDER BY {order_by} {sort}"
        self.log(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def show_columns(self, table: str) -> list:
        cursor = self.connection.cursor()
        sql = f"SHOW COLUMNS FROM {table}"
        cursor.execute(sql)
        self.log(sql)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def fetch_tables(self) -> list:
        if not self.connection.is_connected():
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        self.log("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return tables

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

    def log(self,query:str):
        if hasattr(self, 'console'):
            self.console.setText(query)
        globals()['query'].append(query)