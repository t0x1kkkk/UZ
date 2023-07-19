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
