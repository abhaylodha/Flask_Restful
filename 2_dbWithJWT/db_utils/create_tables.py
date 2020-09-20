import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(users_table)

items_table = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
cursor.execute(items_table)

connection.commit()
connection.close()
