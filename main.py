import sqlite3
import os

# Шлях до файлу бази даних
db_file = 'tickets.db'

# Перевірка, чи файл бази даних існує
if os.path.exists(db_file):
    os.remove(db_file)

# Підключення до бази даних SQLite
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Зчитування SQL-запитів з текстового файлу та їх виконання
with open('create_tables.sql', 'r') as sql_file:
    create_tables_sql = sql_file.read()
    cursor.executescript(create_tables_sql)

# Збереження змін до бази даних
conn.commit()

def search_trains(from_station, to_station):
    # Отримання інформації про поїздки з бази даних
    cursor.execute('''
        SELECT * FROM trains
        WHERE from_station = ? AND to_station = ?
    ''', (from_station, to_station))
    trains = cursor.fetchall()

    # Обробка та відображення інформації про поїздки
    for train in trains:
        print(f"ID поїзда: {train[0]}")
        print(f"З: {train[1]}")
        print(f"До: {train[2]}")
        print(f"Час відправлення: {train[3]}")
        print(f"Час прибуття: {train[4]}")
        print(f"Ціна: {train[5]}")
        print(f"Доступні місця: {train[6]}")
        print('---------------------------')

def show_available_trains():
    # Отримання всіх поїздів з доступними місцями з бази даних і їх відображення
    cursor.execute('SELECT * FROM trains WHERE available_seats > 0')
    available_trains = cursor.fetchall()

    print("Доступні поїзди:")
    for train in available_trains:
        print(f"ID поїзда: {train[0]}")
        print(f"З: {train[1]}")
        print(f"До: {train[2]}")
        print(f"Час відправлення: {train[3]}")
        print(f"Час прибуття: {train[4]}")
        print(f"Ціна: {train[5]}")
        print(f"Доступні місця: {train[6]}")
        print('---------------------------')

def book_ticket(train_id, passenger_name):
    # Отримання інформації про конкретний поїзд за його ID
    cursor.execute('SELECT * FROM trains WHERE id = ?', (train_id,))
    train = cursor.fetchone()

    if train is None:
        print("Поїзд не знайдено.")
        return

    # Перевірка доступних місць
    if train[6] <= 0:
        print("Немає доступних місць.")
        return

    # Зменшення доступних місць та збереження інформації про квиток в базу даних
    cursor.execute('''
        UPDATE trains
        SET available_seats = available_seats - 1
        WHERE id = ?
    ''', (train_id,))

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY,
            from_station TEXT,
            to_station TEXT,
            passenger_name TEXT,
            ticket_price REAL
        )
    ''')

    cursor.execute('''
        INSERT INTO tickets (from_station, to_station, passenger_name, ticket_price)
        VALUES (?, ?, ?, ?)
    ''', (train[1], train[2], passenger_name, train[5]))

    conn.commit()
    print('Квиток успішно заброньовано!')

def show_tickets():
    # Отримання всіх квитків з бази даних і їх відображення
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()

    for ticket in tickets:
        print(f"ID квитка: {ticket[0]}")
        print(f"З: {ticket[1]}")
        print(f"До: {ticket[2]}")
        print(f"Ім'я пасажира: {ticket[3]}")
        print(f"Ціна: {ticket[4]}")
        print('---------------------------')

# Виклик функції показу доступних поїздів
show_available_trains()

# Введення даних користувача
from_station = input("Введіть станцію відправлення: ")
to_station = input("Введіть станцію призначення: ")
passenger_name = input("Введіть ім'я пасажира: ")

# Виклик функції пошуку поїздок
search_trains(from_station, to_station)

# Вибір поїзда та бронювання квитка
train_id = input("Введіть ID поїзда для бронювання квитка: ")
book_ticket(train_id, passenger_name)

# Показ заброньованих квитків
show_tickets()

# Закриття підключення до бази даних
conn.close()
