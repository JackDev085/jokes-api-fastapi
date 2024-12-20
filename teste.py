import sqlite3

conn = sqlite3.connect("db.sqlite3",check_same_thread=False,autocommit=True)

cursor = conn.cursor()
cursor.execute("update categories set name ='humor' where id = 2")