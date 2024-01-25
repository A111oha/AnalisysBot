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


    def commit_query(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
    def insert_data(self, table, columns, values):
        """
        Метод для вставки даних в таблицю.
        :param table: Назва таблиці.
        :param columns: Список назв стовпців, у які ви хочете вставити дані.
        :param values: Список значень, які ви хочете вставити в відповідні стовпці.
        """
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in values])})"
        params = tuple(values)
        self.commit_query(query, params)