# Імпортуємо необхідні бібліотеки

import telebot
from telebot import types
from datetime import datetime
import hashlib
from Database import Database
from Analysis import Analysis
from Operations import Operations
from Parser import Parser
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN =os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
# Створюємо об'єкт бази даних з параметрами підключення
db = Database()
analysis_instance = Analysis()
operations_instance = Operations()
parser_instance = Parser()


# Визначаємо обробник команди /start, яка відправляє привітання
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Початкові кнопки категорій
    item_graphics = types.KeyboardButton("Графіки")
    item_statistics = types.KeyboardButton("Статистика")
    item_operations = types.KeyboardButton("Операції")

    markup.add(item_graphics, item_statistics, item_operations)

    bot.reply_to(message, "Привіт, оберіть категорію:", reply_markup=markup)

# Додаткові кнопки для категорії "Графіки"
@bot.message_handler(func=lambda message: message.text.lower() == 'графіки')
def graphics_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_sales_dynamics_chart = types.KeyboardButton("Графік динаміки продажів")
    item_basket = types.KeyboardButton("Аналіз кошика")
    item_user_country = types.KeyboardButton("Розподіл користувачів за країнами")
    item_product_av = types.KeyboardButton("Доступність товарів за категоріями")
    item_order_frequency = types.KeyboardButton("Частота замовлень")
    item_prognose = types.KeyboardButton("Прогноз")

    # Додайте кнопку "Повернутись"
    item_back = types.KeyboardButton("Повернутись")
    markup.add(item_sales_dynamics_chart, item_basket, item_user_country, item_product_av,
               item_order_frequency,item_prognose, item_back)

    bot.reply_to(message, "Оберіть графік для перегляду:", reply_markup=markup)
# Додаткові кнопки для категорії "Статистика"
@bot.message_handler(func=lambda message: message.text.lower() == 'статистика')
def statistics_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item_query = types.KeyboardButton("Список категорій")
    item_total_sales = types.KeyboardButton("Загальний обсяг продажів")
    item_registered_users = types.KeyboardButton("Кількість користувачів")
    item_user_activity = types.KeyboardButton("Активність користувачів")
    item_most_popular = types.KeyboardButton("Найпопулярніше")
    item_profitability_turnover = types.KeyboardButton("Прибутковість та оборот")

    # Додайте кнопку "Повернутись"
    item_back = types.KeyboardButton("Повернутись")
    markup.add(item_query, item_total_sales, item_registered_users, item_user_activity, item_most_popular,
               item_profitability_turnover, item_back)

    bot.reply_to(message, "Оберіть статистичний запит:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text.lower() == 'операції')
def operation_category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_add_admin = types.KeyboardButton("Додати адміністратора")
    item_delete_admin = types.KeyboardButton("Видалити адміністратора")
    item_parse= types.KeyboardButton("Парсити")


    # Додайте кнопку "Повернутись"
    item_back = types.KeyboardButton("Повернутись")
    markup.add(item_add_admin, item_delete_admin,item_parse, item_back)

    bot.reply_to(message, "Оберіть операцію:", reply_markup=markup)
@bot.message_handler(func=lambda message: message.text.lower() == 'повернутись')
def return_to_start(message):
    send_welcome(message)

# Визначаємо обробник команди query, яка виконує запит до бази даних і відправляє результат
@bot.message_handler(func=lambda message: message.text.lower() == 'список категорій')
def execute_query(message):
    # Виконуємо запит за допомогою методу execute_query класу Database
    result = db.execute_query("SELECT * FROM Category")
    # Форматуємо результат у рядок, розділяючи значення комами
    result_str = "\n".join([". ".join(map(str, row)) for row in result])
    # Відправляємо результат користувачеві
    bot.reply_to(message, result_str)

# Визначаємо обробник команди total_sales
@bot.message_handler(func=lambda message: message.text.lower() == 'загальний обсяг продажів')
def total_sales_command(message):
    # Викликаємо метод total_sales з класу Analysis
    start_date = "2023-06-11"
    end_date = "2024-01-13"
    total_sales_result = analysis_instance.total_sales(start_date, end_date)
    bot.reply_to(message, f"Загальний обсяг продажів за період з {start_date} по {end_date}: {total_sales_result}")

# Визначаємо обробник команди sales_dynamics_chart
@bot.message_handler(func=lambda message: message.text.lower() == 'графік динаміки продажів')
def sales_dynamics_chart_command(message):
    # Викликаємо метод sales_dynamics_chart з класу Analysis
    buffer = analysis_instance.sales_dynamics_chart()
    # Відправляємо графік через бота
    bot.send_photo(message.chat.id, photo=buffer)
    # Відправляємо повідомлення про успішне побудовання графіку
    bot.reply_to(message, "Побудовано графік динаміки продажів.")
# Визначаємо обробник команди total_registered_users
@bot.message_handler(func=lambda message: message.text.lower() == 'кількість користувачів')
def total_registered_users_command(message):
    # Викликаємо метод total_registered_users з класу Analysis
    total_users = analysis_instance.total_registered_users()
    # Відправляємо результат користувачеві
    bot.reply_to(message, f"Кількість  користувачів: {total_users}")

@bot.message_handler(func=lambda message: message.text.lower() == 'активність користувачів')
def user_activity_command(message):
    # Викликаємо метод user_activity з класу Analysis
    user_activity_result = analysis_instance.user_activity()

    bot.reply_to(message, user_activity_result)

@bot.message_handler(func=lambda message: message.text.lower() == 'найпопулярніше')
def most_popular_command(message):
    result_manufacturers, result_categories = analysis_instance.most_popular_manufacturers_and_categories()

    # Формуємо повідомлення для виведення результату
    message_text = "Найпопулярніші виробники:\n"
    message_text += "\n".join([f"{row[0]} - Кількість товарів: {row[1]}" for row in result_manufacturers])

    message_text += "\n\nНайпопулярніші категорії:\n"
    message_text += "\n".join([f"{row[0]} - Кількість товарів: {row[1]}" for row in result_categories])

    # Виводимо результат у телеграм-чат
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(func=lambda message: message.text.lower() == 'прибутковість та оборот')
def profitability_and_turnover_command(message):
    result_manufacturers, result_categories = analysis_instance.profitability_and_turnover_comparison()

    # Формуємо повідомлення для виведення результату
    message_text = "Порівняння прибутковості та обороту:\n"

    message_text += "\nВиробники:\n"
    message_text += "\n".join(
        [f"{row[0]} - Загальний оборот: {row[1]}, Середнє значення замовлення: {row[2]}" for row in
         result_manufacturers])

    message_text += "\nКатегорії:\n"
    message_text += "\n".join(
        [f"{row[0]} - Загальний оборот: {row[1]}, Середнє значення замовлення: {row[2]}" for row in result_categories])

    # Виводимо результат у телеграм-чат
    bot.send_message(message.chat.id, message_text)
@bot.message_handler(func=lambda message: message.text.lower() == 'аналіз кошика')
def basket_command(message):
    buffer = analysis_instance.basket_analysis()
    bot.send_photo(message.chat.id, photo=buffer)


@bot.message_handler(func=lambda message: message.text.lower() == 'розподіл користувачів за країнами')
def user_country_command(message):
    buffer = analysis_instance.user_country_distribution()
    bot.send_photo(message.chat.id, photo=buffer)

@bot.message_handler(func=lambda message: message.text.lower() == 'доступність товарів за категоріями')
def product_availability_command(message):
    buffer = analysis_instance.product_availability_chart()
    bot.send_photo(message.chat.id, photo=buffer)

@bot.message_handler(func=lambda message: message.text.lower() == 'частота замовлень')
def order_frequency_command(message):
    buffer = analysis_instance.user_order_frequency_chart()
    bot.send_photo(message.chat.id, photo=buffer)

@bot.message_handler(func=lambda message: message.text.lower() == 'прогноз')
def prognose_command(message):
    df = analysis_instance.fetch_data()
    model = analysis_instance.train_model(df)
    forecast_df = analysis_instance.forecast_future_sales(model, df, num_days=30)
    buffer_actual, buffer_forecast = analysis_instance.plot_results(df, forecast_df)
    # Відправка фото для поточних продаж
    bot.send_photo(message.chat.id, photo=buffer_actual)
    # Відправка фото для прогнозованих продаж
    bot.send_photo(message.chat.id, photo=buffer_forecast)

@bot.message_handler(func=lambda message: message.text.lower() == 'додати адміністратора')
def add_admin_command(message):
    try:
        # Виводимо повідомлення з порядком вводу значень
        bot.send_message(message.chat.id, "Будь ласка, введіть дані адміністратора в наступному порядку:\n"
                                          "Ім'я Прізвище Країна Місто Логін\n"
                                          "Наприклад: John Doe USA New York john_doe")

        # Чекаємо на введення даних користувачем
        bot.register_next_step_handler(message, process_admin_data)
    except Exception as e:
        bot.reply_to(message, f"Помилка при додаванні адміністратора: {e}")
def process_admin_data(message):
    try:
        # Отримуємо дані від користувача
        data = message.text.split()
        # Перевіряємо, чи користувач ввів усі необхідні поля
        if len(data) != 5:
            bot.reply_to(message, "Будь ласка, введіть всі необхідні поля.")
            return
        # Розпаковуємо дані
        first_name, last_name, country, city, login = data
        access = 1
        # Генеруємо випадковий пароль
        generated_password = operations_instance.generate_random_password()
        # Шифруємо пароль з використанням bcrypt
        hashed_password = hashlib.md5(generated_password.encode('utf-8')).hexdigest()
        # Отримуємо поточну дату
        register_date = datetime.now().strftime("%Y-%m-%d")
        if(operations_instance.check_user_existence(login)):
            bot.reply_to(message, f"Користувач із логіном {login} вже існує.")
        else:
            operations_instance.add_user(first_name, last_name, hashed_password, country, city, access, login,
                                         register_date)
            bot.reply_to(message,
                         f"Адміністратор {first_name} {last_name} доданий успішно. Згенерований пароль: {generated_password}")
    except Exception as e:
        print(f"Помилка при додаванні адміністратора: {e}")

@bot.message_handler(func=lambda message: message.text.lower() == 'видалити адміністратора')
def delete_admin_command(message):
    try:
        # Виводимо повідомлення з порядком вводу значень
        bot.send_message(message.chat.id, "Будь ласка, введіть логін адміністратора")
        # Чекаємо на введення даних користувачем
        bot.register_next_step_handler(message, process_admin_data_del)
    except Exception as e:
        print(f"Помилка при видаленні адміністратора: {e}")
def process_admin_data_del(message):
    try:
        # Отримуємо дані від користувача
        data = message.text
        login = data
        if(operations_instance.check_user_existence(login)):
            operations_instance.delete_user(login)
            bot.reply_to(message,
                         f"Адміністратора {login} успішно видалено")
        else:
            bot.reply_to(message, f"Користувач із логіном {login} не існує.")

    except Exception as e:
        print(f"Помилка при видаленні адміністратора: {e}")

@bot.message_handler(func=lambda message: message.text.lower() == 'парсити')
def parse(message):
    try:
        url_to_parse = 'https://rozetka.com.ua/ua/fishing/c84703/'
        parsed_data = parser_instance.parse_website(url_to_parse)
        bot.send_message(message.chat.id, "5 Найпопулярніших товарів на інших сайтах:")

        # Відправляємо зібрані дані користувачеві
        for i, data in enumerate(parsed_data):
            response_text = f"{i + 1}.\nUrl - {data['url']}\nName - {data['name']}\nPrice - {data['price']}\n\n"
            bot.send_message(message.chat.id, response_text)
    except Exception as e:
        print(f"Помилка при парсингу: {e}")
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Вибачте, але я поки не знаю цю команду. Спробуйте іншу команду.")
# Запускаємо бота, щоб він слухав повідомлення
bot.polling()

