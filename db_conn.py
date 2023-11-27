import sqlite3

DATABASE_NAME = "local_storage.db"
conn = sqlite3.connect(DATABASE_NAME)
cur = conn.cursor()
