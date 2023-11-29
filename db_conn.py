import sqlite3

WORKING_PATH = r'C:\\Users\\Diego\\Journey\\School\\IoT\\Intelligent Classroom\\'

DATABASE_NAME = "local_storage.db"
conn = sqlite3.connect(DATABASE_NAME)
cur = conn.cursor()
