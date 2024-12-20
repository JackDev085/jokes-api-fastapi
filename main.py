from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from db.connection import Connection
from repository.JokesRepository import JokesRepository
from models.Joke import Joke
from random import randint
from fastapi.middleware.cors import CORSMiddleware


# Conexão com o banco de dados e inicialização do repositório
cursor = Connection("db.sqlite3")
jokes_repository = JokesRepository(cursor)

# Instância do FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def all_jokes():
    all_jokes = jokes_repository.fetch_all()
    return {"aleatory joke": all_jokes[randint(0, len(all_jokes))-1],
            "routes":[
                {1:"api/jokes/ - all jokes"},
                {2:"api/jokes/{id} - one joke by id"},
                {3:"api/jokes/c/category?category={category} - jokes by category"}
            ]
        }



# Rota para buscar uma piada pelo ID
@app.get("/api/jokes/{id}")
def one_joke(id: int):
    joke = jokes_repository.fetch_one(id)
    if joke is None:
        return HTTPException(status_code=404, detail="Joke not found")
    return {"joke": joke}

# Rota para buscar todas as piadas
@app.get("/api/jokes/")
def all_jokes():
    all_jokes = jokes_repository.fetch_all()
    return {"jokes": all_jokes}

# Rota para buscar piadas por categoria
@app.get("/api/jokes/c/category/")
def all_jokes_by_category(category: Optional[str] = Query(None)):
    if category is not None and category != "":
        all_by_category = jokes_repository.fetch_all_by_category(category)
        if all_by_category:
                return {f"jokes - {category}": all_by_category}
    return {"error": "category not found"}

# Rota para deletar uma piada pelo ID (opcional, se necessário)
@app.delete("/api/jokes/{id}")
def delete_one(id: int):
    joke = jokes_repository.fetch_one(id)
    if joke is None:
        raise HTTPException(status_code=404, detail="Joke not found")
    jokes_repository.delete_one(id)
    return {"deleted_joke": joke}

# Rota para atualizar uma piada pelo ID (opcional, se necessário)
@app.put("/api/jokes/{id}")
def update_one(joke: Joke, id: int):
    updated_joke = jokes_repository.update_one(joke, id)
    if updated_joke is None:
        raise HTTPException(status_code=404, detail="Joke not found")
    return {"updated_joke": updated_joke}

@app.post("/api/jokes/create/")
def update_one(joke: Joke):
    created_joke = jokes_repository.create_one(joke)
    if created_joke is None:
        raise HTTPException(status_code=500, detail="Error during create joke")
    return {"created_joke": created_joke}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8080, host='0.0.0.0')
"""@app.delete("/api/jokes/{id}")
def delete_one(id:int):
    deleted = jokes_repository.fetch_one(id)
    jokes_repository.delete_one(id)
    return {"deleted_joke":deleted}

@app.put("/api/jokes/{id}")
def update_one(joke:Joke,id:int):
    all = jokes_repository.update_one(joke,id)
    return {"jokes":all}"""