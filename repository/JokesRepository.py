from db.connection import Connection
from models.Joke import Joke

class JokesRepository:
    def __init__(self, cursor: Connection):
        self._cursor = cursor

    def fetch_all(self):
        try:
            sql = """select jokes.id, ask, response, name from jokes
            inner join categories on jokes.category_id = categories.id where jokes.id > 0
            """
            self._cursor.execute_query(sql)
            result = self._cursor.fetch_all()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def fetch_all_by_category(self, category:str):
        try:
            sql = """
            select jokes.id, ask, response, name from jokes
            inner join categories on jokes.category_id = categories.id
            where name = (?)
            """
            self._cursor.execute_query(sql, (category,))
            result = self._cursor.fetch_all()
            if len(result) < 0:
                return None
            
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def fetch_one(self, id: int):
        try:
            sql = """
            select jokes.id, ask, response, name from jokes
            inner join categories on jokes.category_id = categories.id 
            where jokes.id = ?
            """
            self._cursor.execute_query(sql, (id,))
            result = self._cursor.fetch_one()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def delete_one(self, id: int):
        try:
            sql = """
            delete from jokes where id = (?)
            """
            return self._cursor.execute_query(sql, (id,))
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def update_one(self, joke:Joke,id:int):
        try:
            sql = """
            update jokes set ask = (?), response = (?), category_id = (?) where id = (?)
            """
            self._cursor.execute_query(sql, (joke.ask, joke.response, joke.category_id,id))
            return self._cursor.execute_query("select * from jokes where id=(?)",(id,)).fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def create_one(self,joke:Joke):
        try:
            sql = """
            insert into jokes(ask,response,category_id) values(?,?,?)
            """
            self._cursor.execute_query(sql,(joke.ask,joke.response,joke.category_id))
            return self._cursor.execute_query("select * from jokes where id=(select max(id) from jokes)").fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None