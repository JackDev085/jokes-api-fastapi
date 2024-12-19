import sqlite3 

conn = sqlite3.connect("db.sqlite3")
cursor = conn.execute("ALTER TABLE jokes rename column catogory_id to category_id")