import mysql.connector
from mysql.connector import Error

class MySQLConnect:
    def __init__(self, host: str, user: str, password: str):
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.query = self.fetch_databases("SHOW DATABASES")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.query = []

    def use_database(self, database: str):
        cursor = self.mydb.cursor()
        cursor.execute(f"USE {database}")
        cursor.close()

    def fetch_databases(self, sql: str):
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        databases = cursor.fetchall()
        cursor.close()
        return databases
    
    def fetch_tables(self) -> list:
        if not self.mydb.is_connected():
            return []
        
        cursor = self.mydb.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        return tables

    def close_connection(self):
        if self.mydb.is_connected():
            self.mydb.close()
