from fastapi import FastAPI
from db.connection import Connection
from repository.JokesRepository import JokesRepository

cursor = Connection("db.sqlite3")
jokes_repository = JokesRepository(cursor)
app = FastAPI()

@app.get("/api/jokes")
def all_jokes():
    all = jokes_repository.fetch_all()
    return {"jokes":all}