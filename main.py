# Імпортуємо необхідні бібліотеки
import os
import io
import base64
import telebot
from Database import Database # Імпортуємо ваш клас Database з файлу database.py
from Analysis import Analysis

# Створюємо об'єкт бота з токеном, який отримали від @BotFather
TOKEN = '6388346527:AAGsbSDQbQBuBV_OunDcJX_ORsIt_e0T9Ug'
bot = telebot.TeleBot(TOKEN)
# Створюємо об'єкт бази даних з параметрами підключення
db = Database()
analysis_instance = Analysis()

# Визначаємо обробник команди /start, яка відправляє привітання
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, я телеграм бот, який взаємодіє з базою даних.")

# Визначаємо обробник команди /query, яка виконує запит до бази даних і відправляє результат
@bot.message_handler(commands=['query'])
def execute_query(message):
    # Виконуємо запит за допомогою методу execute_query класу Database
    result = db.execute_query("SELECT * FROM Category")
    # Форматуємо результат у рядок, розділяючи значення комами
    result_str = "\n".join([". ".join(map(str, row)) for row in result])
    # Відправляємо результат користувачеві
    bot.reply_to(message, result_str)
@bot.message_handler(commands=['total_sales'])
def total_sales_command(message):
    # Викликаємо метод total_sales з класу Analysis
    start_date = "2023-06-11"
    end_date = "2023-06-14"
    total_sales_result = analysis_instance.total_sales(start_date, end_date)
    bot.reply_to(message, f"Загальний обсяг продажів за період: {total_sales_result}")

# Визначаємо обробник команди /sales_dynamics_chart
@bot.message_handler(commands=['sales_dynamics_chart'])
def sales_dynamics_chart_command(message):
    # Викликаємо метод sales_dynamics_chart з класу Analysis
    buffer = analysis_instance.sales_dynamics_chart()
    # Відправляємо графік через бота
    bot.send_photo(message.chat.id, photo=buffer)
    # Відправляємо повідомлення про успішне побудовання графіку
    bot.reply_to(message, "Побудовано графік динаміки продажів.")


@bot.message_handler(commands=['total_registered_users'])
def total_registered_users_command(message):
    # Викликаємо метод total_registered_users з класу Analysis
    total_users = analysis_instance.total_registered_users()
    # Відправляємо результат користувачеві
    bot.reply_to(message, f"Загальна кількість зареєстрованих користувачів: {total_users}")

@bot.message_handler(commands=['user_activity'])
def user_activity_command(message):
    # Викликаємо метод user_activity з класу Analysis
    user_activity_result = analysis_instance.user_activity()
    # Форматуємо результат у рядок, розділяючи значення комами
    #result_str = "\n".join([" ".join(map(str, row)) for row in user_activity_result])
    # Відправляємо результат користувачеві
    bot.reply_to(message, user_activity_result)


@bot.message_handler(commands=['most_popular'])
def most_popular_command(message):
    result_manufacturers, result_categories = analysis_instance.most_popular_manufacturers_and_categories()

    # Формуємо повідомлення для виведення результату
    message_text = "Найпопулярніші виробники:\n"
    message_text += "\n".join([f"{row[0]} - Кількість товарів: {row[1]}" for row in result_manufacturers])

    message_text += "\n\nНайпопулярніші категорії:\n"
    message_text += "\n".join([f"{row[0]} - Кількість товарів: {row[1]}" for row in result_categories])

    # Виводимо результат у телеграм-чат
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=['profitability_and_turnover'])
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



# Запускаємо бота, щоб він слухав повідомлення
bot.polling()

