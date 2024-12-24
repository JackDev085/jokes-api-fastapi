from db.connection import Connection
from models.Joke import Joke
from random import randint

class JokesRepository:
    def __init__(self, cursor: Connection):
        self._cursor = cursor

    def fetch_all(self):
        try:
            sql = """
            SELECT jokes.id, jokes.ask, jokes.response, category_name
            FROM jokes 
            INNER JOIN categories ON jokes.category_id = categories.id;
            """
            self._cursor.execute_query(sql)
            return self._cursor.fetch_all()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def fetch_aleatory(self,) ->list:
        count_number = self.count_jokes()
        aleatory = randint(1,count_number[0])
        print(aleatory)
        try:
            sql = """
            SELECT jokes.id, jokes.ask, jokes.response, category_name
            FROM jokes 
            INNER JOIN categories ON jokes.category_id = categories.id
            WHERE jokes.id = (?)
            """
            self._cursor.execute_query(sql,(aleatory,))
            return self._cursor.fetch_all()
        except Exception as e:
            print(f"An error occurred fetch_aleatory: {e}")
            return None

        
    def count_jokes(self):
        try:
            sql = """
            select count(*) from jokes
            """
            self._cursor.execute_query(sql)
            return self._cursor.fetch_one()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def fetch_all_by_category(self, category:str):
        try:
            sql = """
            SELECT jokes.id, jokes.ask, jokes.response, category_name FROM jokes
            INNER JOIN categories ON jokes.category_id = categories.id
            where category_name = (?)
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
            select jokes.id, ask, response, category_name from jokes
            INNER JOIN categories ON jokes.category_id = categories.id;
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
            update jokes set ask = (?), response = (?), category_name = (?) where id = (?)
            """
            self._cursor.execute_query(sql, (joke.ask, joke.response, joke.category_name,id))
            return self._cursor.execute_query("select * from jokes where id=(?)",(id,)).fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def create_one(self,joke:Joke):
        try:
            sql = """
            insert into jokes(ask,response,category_name) values(?,?,?)
            """
            self._cursor.execute_query(sql,(joke.ask,joke.response,joke.category_name,))
            return self._cursor.execute_query("select * from jokes where id=(select max(id) from jokes)").fetchone()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def count(self):
        try:
            sql = """
            select * from jokes
            """
            self._cursor.execute_query(sql)

            return len(self._cursor.fetch_all())
        except Exception as e:
            print(f"An error occurred: {e}")
            return None