import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
from Database import Database
class Analysis:
    db = Database()
    def total_sales(self,start_date, end_date,):
        query = f"SELECT SUM(TotalAmount) FROM Orders WHERE OrderDate BETWEEN '{start_date}' AND '{end_date}';"
        result =Analysis.db.execute_query(query)
        return result[0][0] if result[0][0] else 0
    def sales_dynamics_chart(self):
        query = "SELECT OrderDate, SUM(TotalAmount)  FROM Orders GROUP BY OrderDate;"
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['OrderDate', 'TotalSales'])
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        df.set_index('OrderDate', inplace=True)
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['TotalSales'], marker='o')
        plt.title('Sales Dynamics')
        plt.xlabel('Order Date')
        plt.ylabel('Total Sales')
        plt.grid(True)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def total_registered_users(self):
        query = "SELECT COUNT(*) FROM Users;"
        result = Analysis.db.execute_query(query)
        return result[0][0] if result[0][0] else 0

    def user_activity(self):
        query = """
            SELECT Users.id_User, COUNT(Orders.id_Order) as order_count, SUM(Orders.TotalAmount) as total_spent
            FROM Users
            LEFT JOIN Orders ON Users.id_User = Orders.id_User
            GROUP BY Users.id_User;
        """
        result = Analysis.db.execute_query(query)
        # Створюємо DataFrame
        df = pd.DataFrame(result, columns=['UserID', 'OrderCount', 'TotalSpent'])
        # Форматуємо результат у рядок вручну
        result_str = "UserID    OrderCount    TotalSpent\n"
        result_str += "-" * 40 + "\n"
        for row in df.itertuples(index=False):
            result_str += f"{row.UserID:<10} {row.OrderCount:<15} {row.TotalSpent:<15}\n"
        return result_str

    def most_popular_manufacturers_and_categories(self):
        # Визначення найпопулярніших виробників та категорій серед вже куплених товарів
        query_manufacturers = """
             SELECT m.Name, COUNT(*) as total_products
        FROM Orders o
        JOIN Product p ON o.id_Product = p.id_Product
        JOIN Manufacturer m ON p.id_Manufacturer = m.id_Manufacturer
        GROUP BY m.Name
        ORDER BY total_products DESC
        LIMIT 5;
        """
        query_categories = """
            SELECT c.Name, COUNT(*) as total_products
        FROM Orders o
        JOIN Product p ON o.id_Product = p.id_Product
        JOIN Category c ON p.id_Category = c.id_Category
        GROUP BY c.Name
        ORDER BY total_products DESC
        LIMIT 5;
        """

        result_manufacturers = Analysis.db.execute_query(query_manufacturers)
        result_categories = Analysis.db.execute_query(query_categories)

        return result_manufacturers, result_categories

    def profitability_and_turnover_comparison(self):
        # Порівняння прибутковості та обороту між різними виробниками та категоріями
        query_manufacturers = """
            SELECT m.Name, SUM(o.TotalAmount) as total_turnover, AVG(o.TotalAmount) as average_order_value
            FROM Orders o
            JOIN Product p ON o.id_Product = p.id_Product
            JOIN Manufacturer m ON p.id_Manufacturer = m.id_Manufacturer
            GROUP BY m.Name;
        """

        query_categories = """
            SELECT c.Name, SUM(o.TotalAmount) as total_turnover, AVG(o.TotalAmount) as average_order_value
            FROM Orders o
            JOIN Product p ON o.id_Product = p.id_Product
            JOIN Category c ON p.id_Category = c.id_Category
            GROUP BY c.Name;
        """

        result_manufacturers = Analysis.db.execute_query(query_manufacturers)
        result_categories = Analysis.db.execute_query(query_categories)

        return result_manufacturers, result_categories



