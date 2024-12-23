import sqlite3

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
count = cursor.execute('select count(*) from jokes').fetchone()[0]
print(count)