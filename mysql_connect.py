import mysql.connector
from mysql.connector import Error

class MySQLConnect:
    def __init__(self, host: str, user: str, password: str):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.databases = self._fetch_databases("SHOW DATABASES")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.databases = []

    def use_database(self, database: str):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {database}")
        cursor.close()

    def _fetch_databases(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        databases = cursor.fetchall()
        cursor.close()
        return databases
    
    def fetch_tables(self) -> list:
        if not self.connection.is_connected():
            return []
        
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return tables

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()