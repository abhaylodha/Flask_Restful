import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

user = ("admin", "Admin@1234")
insert_query = "INSERT INTO users VALUES (null, ?, ?)"
cursor.execute(insert_query, user)

connection.commit()
connection.close()
