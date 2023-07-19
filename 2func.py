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
