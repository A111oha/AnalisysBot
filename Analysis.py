import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
from Database import Database
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
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

    def basket_analysis(self):
        # Аналіз кошиків користувачів: середня ціна та кількість товарів у кошику
        query = """
                SELECT id_User, AVG(AllPrice) as average_price, AVG(Quantity) as average_quantity
                FROM Basket
                GROUP BY id_User;
            """
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['UserID', 'AveragePrice', 'AverageQuantity'])

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x=df['AverageQuantity'], y=df['AveragePrice'], alpha=0.7)
        plt.title('Basket Analysis')
        plt.xlabel('Average Quantity in Basket')
        plt.ylabel('Average Price in Basket')
        plt.grid(True)
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def product_availability_chart(self):
        # Графік доступності товарів у категоріях
        query = """
                SELECT c.Name as Category, COUNT(p.id_Product) as TotalProducts
                FROM Product p
                JOIN Category c ON p.id_Category = c.id_Category
                GROUP BY c.Name;
            """
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['Category', 'TotalProducts'])

        plt.figure(figsize=(12, 8))
        sns.barplot(x=df['Category'], y=df['TotalProducts'], palette='Set2')
        plt.title('Product Availability by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Products')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def user_country_distribution(self):
        # Розподіл користувачів за країною
        query = """
                SELECT Country, COUNT(id_User) as UserCount
                FROM Users
                GROUP BY Country;
            """
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['Country', 'UserCount'])

        plt.figure(figsize=(12, 8))
        sns.barplot(x=df['UserCount'], y=df['Country'], orient='h')
        plt.title('User Country Distribution')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer



    def manufacturer_distribution_chart(self):
        # Графік розподілу товарів за виробниками
        query = """
               SELECT m.Name as Manufacturer, COUNT(p.id_Product) as TotalProducts
               FROM Product p
               JOIN Manufacturer m ON p.id_Manufacturer = m.id_Manufacturer
               GROUP BY m.Name;
           """
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['Manufacturer', 'TotalProducts'])

        plt.figure(figsize=(12, 8))
        plt.bar(df['Manufacturer'], df['TotalProducts'], color='lightgreen')
        plt.title('Manufacturer Distribution Chart')
        plt.xlabel('Manufacturer')
        plt.ylabel('Total Products')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def user_order_frequency_chart(self):
        # Графік частоти замовлень для кожного користувача
        query = """
               SELECT id_User, COUNT(id_Order) as OrderCount
               FROM Orders
               GROUP BY id_User;
           """
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['UserID', 'OrderCount'])

        plt.figure(figsize=(12, 8))
        plt.bar(df['UserID'], df['OrderCount'], color='salmon')
        plt.title('User Order Frequency Chart')
        plt.xlabel('User ID')
        plt.ylabel('Order Count')
        plt.grid(axis='y')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer

    def train_model(self, df):
        # Розбийте дані на тренувальний та тестовий набори
        train, test = train_test_split(df, test_size=0.2, shuffle=False)

        # Навчайте модель
        model = LinearRegression()
        X_train = pd.to_numeric(train['OrderDate'].values)
        y_train = train['OrderCount'].values
        model.fit(X_train.reshape(-1, 1), y_train)

        # Перевірка точності моделі на тестовому наборі
        X_test = pd.to_numeric(test['OrderDate'].values)
        y_test = test['OrderCount'].values
        predictions = model.predict(X_test.reshape(-1, 1))
        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')

        return model

    def forecast_future_sales(self, model, df, num_days):
        # Генеруємо майбутні дати
        last_date = df['OrderDate'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=num_days, freq='D')
        print(future_dates)

        # Перетворюємо дати в числовий формат для моделі
        future_dates_numeric = pd.to_numeric(future_dates.values)

        # Прогнозуємо майбутні продажі
        future_sales = model.predict(future_dates_numeric.reshape(-1, 1))

        # Створюємо DataFrame для відображення результатів
        forecast_df = pd.DataFrame({'Date': future_dates, 'ForecastedSales': future_sales})
        forecast_df.set_index('Date', inplace=True)

        return forecast_df

    def fetch_data(self):
        # Зчитайте дані з бази даних
        query = "SELECT OrderDate, COUNT(id_Order) as OrderCount FROM Orders GROUP BY OrderDate;"
        result = Analysis.db.execute_query(query)
        df = pd.DataFrame(result, columns=['OrderDate', 'OrderCount'])
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        return df

    def plot_results(self, df, forecast_df):
        # Перетворення дат в однаковий формат
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        forecast_df.index = pd.to_datetime(forecast_df.index)

        # Графік для поточних продаж
        plt.figure(figsize=(12, 6))
        plt.plot(df['OrderDate'], df['OrderCount'], label='Actual Sales', marker='o')
        plt.title('Actual Sales')
        plt.xlabel('Date')
        plt.ylabel('Sales Count')
        plt.legend()
        plt.grid(True)
        buffer_actual = io.BytesIO()
        plt.savefig(buffer_actual, format='png')
        buffer_actual.seek(0)

        # Графік для прогнозованих продаж
        plt.figure(figsize=(12, 6))
        plt.plot(forecast_df.index, forecast_df['ForecastedSales'], label='Forecasted Sales', linestyle='--',
                 marker='o')
        plt.title('Sales Forecasting')
        plt.xlabel('Date')
        plt.ylabel('Sales Count')
        plt.legend()
        plt.grid(True)
        buffer_forecast = io.BytesIO()
        plt.savefig(buffer_forecast, format='png')
        buffer_forecast.seek(0)
        return buffer_actual, buffer_forecast
