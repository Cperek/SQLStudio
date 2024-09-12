import sys
import mysql.connector


class MySQLConnect:


    def __init__(self, host, user, password):

        mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )

        query = mydb.cursor()
        query.execute("SHOW DATABASES")
        self.query = query.fetchall()
