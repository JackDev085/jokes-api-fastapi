from db.connection import Connection
class JokesRepository:
    def __init__(self, cursor:Connection):
        self._cursor = cursor

    def fetch_all(self):
        self._cursor.execute_query("""select jokes.id, ask,response,name from jokes inner join categories on jokes.category_id = categories.id""")
        result = self._cursor.fetch_all()
        return result
    
    def fetch_one(self):
        self._cursor.execute_query("""select jokes.id, ask,response,name from jokes inner join categories on jokes.category_id = categories.id""")
        result = self._cursor.fetch_all()
        return result

