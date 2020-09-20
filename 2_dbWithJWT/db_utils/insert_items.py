import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

user = ("Chair", 500)
insert_query = "INSERT INTO items VALUES (?, ?)"
cursor.execute(insert_query, user)

connection.commit()
connection.close()
