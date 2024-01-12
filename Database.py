import mysql.connector
class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="MyStore"
        )

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insert_data(self, table, data):
        cursor = self.connection.cursor()
        query = f"INSERT INTO {table} VALUES ({data})"
        cursor.execute(query)
        self.connection.commit()
