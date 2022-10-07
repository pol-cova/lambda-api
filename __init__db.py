import sqlite3

try:
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    print("[*] Database conection!")

    query = """INSERT INTO users
        (id, fullname, username, password, email)
        VALUES
        (1, 'pol', 'polc', 'pol*', 'test@example.com')"""

    count = cur.execute(query)
    connection.commit()
    print("Succesfully data insert")
    cur.close()
except sqlite3.Error as error:
    print("[*] Fatal error!", error)
finally:
    if connection:
        connection.close()
        print("[*] Connection is closed now!")


