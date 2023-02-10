import mysql.connector
from einst import *


class Database():
    def __init__(self):
        self.db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            database=db_name
        )
        self.cursor = self.db.cursor()

    def get_all(self):
        self.cursor.execute("SELECT * FROM driver")
        return self.cursor.fetchall()

    def __del__(self):
        self.db.close()
