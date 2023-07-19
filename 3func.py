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
