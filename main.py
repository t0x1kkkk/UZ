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
