import sqlite3 

conn = sqlite3.connect('db.sqlite3')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("""
SELECT jokes.id, jokes.ask, jokes.response,category_name 
            FROM jokes 
            INNER JOIN categories ON jokes.category_id = categories.id
""")
print((cursor.fetchall()[1]))