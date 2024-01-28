from Database import Database
import random
import string
class Operations:
    db = Database()
    def add_user(self, first_name, last_name, hashed_password, country, city, access, login, register_date):
            table = "Users"
            columns_list = ["FirstName", "LastName", "Password", "Country", "City", "Access", "Login", "RegisterDate"]
            values_list = [first_name, last_name, hashed_password, country, city, access, login, register_date]
            Operations.db.insert_data(table, columns_list, values_list)
            print("Користувач успішно доданий.")
    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    def check_user_existence(self, login):
        query = f"SELECT *  FROM Users WHERE Login = '{login}';"
        result = Operations.db.execute_query(query)
        return bool(result)

    def delete_user(self, login):
        table = "Users"
        column = "Login"
        Operations.db.delete_data(table, column, login)


