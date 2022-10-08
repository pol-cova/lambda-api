import sqlite3

try:
    connection = sqlite3.connect('users.db')
    cur = connection.cursor()
    print("[*] Database conection!")
    
    querym = """
    CREATE TABLE users (
    id serial PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL);"""
    ex = cur.execute(querym)
    connection.commit()
    print("[*] Succesfully table created!")
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


