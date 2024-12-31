import sqlite3

connection = sqlite3.connect('ewallet_database.db')
cursor = connection.cursor()

try:
    cursor.execute('SELECT * FROM user_balance')
    result = cursor.fetchall()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()


    print(result)
    print(users)
except Exception as e:
    print(e)
