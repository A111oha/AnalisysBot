from Database import Database
import random
import string
class Operations:
    db = Database()

    def add_user(self, first_name, last_name, hashed_password, country, city, access, login, register_date):
        query = "INSERT INTO Users (FirstName, LastName, Password, Country, City, Access, Login, RegisterDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        values = (first_name, last_name, hashed_password, country, city, access, login, register_date)
        table = "Users"
        columns_list = ["FirstName", "LastName", "Password","Country", "City", "Access","Login", "RegisterDate"]
        values_list = [first_name, last_name, hashed_password, country, city, access, login, register_date]
        Operations.db.insert_data(table, columns_list, values_list)

    def generate_random_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))