import sqlite3

def create_tables():
    # Підключення до бази даних SQLite
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()

    # Створення таблиці для зберігання інформації про поїзди
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            id INTEGER PRIMARY KEY,
            from_station TEXT,
            to_station TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            price REAL,
            available_seats INTEGER
        )
    ''')

    # Створення таблиці для зберігання інформації про заброньовані квитки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booked_tickets (
            id INTEGER PRIMARY KEY,
            train_id INTEGER,
            passenger_name TEXT,
            FOREIGN KEY (train_id) REFERENCES trains (id)
        )
    ''')


    # Перевірка, чи база даних містить поїзди; якщо ні, то додаємо вигадані поїзди
    cursor.execute('SELECT COUNT(*) FROM trains')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executescript(create_trains_sql)

    # Збереження змін до бази даних
    conn.commit()

    # Закриття підключення до бази даних
    conn.close()

def show_available_trains():
    # Отримання всіх поїздів з доступними місцями з бази даних і їх відображення
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
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

    # Закриття підключення до бази даних
    conn.close()

def book_ticket(train_id, passenger_name):
    # Отримання інформації про конкретний поїзд за його ID
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
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
        INSERT INTO booked_tickets (train_id, passenger_name)
        VALUES (?, ?)
    ''', (train_id, passenger_name))

    conn.commit()
    print('Квиток успішно заброньовано!')

    # Закриття підключення до бази даних
    conn.close()

def show_tickets():
    # Отримання всіх заброньованих квитків з бази даних і їх відображення
    conn = sqlite3.connect('tickets.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT trains.from_station, trains.to_station, trains.departure_time, trains.price, booked_tickets.passenger_name
        FROM trains
        JOIN booked_tickets ON trains.id = booked_tickets.train_id
    ''')
    tickets = cursor.fetchall()

    print("Заброньовані квитки:")
    for ticket in tickets:
        print(f"З: {ticket[0]}")
        print(f"До: {ticket[1]}")
        print(f"Час відправлення: {ticket[2]}")
        print(f"Ціна: {ticket[3]}")
        print(f"Ім'я пасажира: {ticket[4]}")
        print('---------------------------')

    # Закриття підключення до бази даних
    conn.close()

if __name__ == "__main__":
    create_tables()
    show_available_trains()

    while True:
        choice = input("Бажаєте забронювати квиток? (Так/Ні): ").strip().lower()
        if choice == 'так':
            train_id = input("Введіть ID поїзда для бронювання квитка: ")
            passenger_name = input("Введіть ім'я пасажира: ")
            book_ticket(train_id, passenger_name)
        elif choice == 'ні':
            break
        else:
            print("Будь ласка, введіть 'Так' або 'Ні'.")

    show_tickets()
