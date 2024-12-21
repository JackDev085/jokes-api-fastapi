from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from db.connection import Connection
from repository.JokesRepository import JokesRepository
from models.Joke import Joke
from random import randint
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


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
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jokes API Frontend</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f4f4f9;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 96vh;
            }

            h1,
            h2 {
                text-align: center;
            }

            p {
                font-weight: 300;
            }

            p,
            strong {
                font-weight: 500;
            }

            #controls {
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-bottom: 20px;
            }

            input,
            button {
                padding: 10px;
                font-size: 16px;
            }

            .jokes-container {
                max-width: 800px;
                margin: 0 auto;
            }

            .joke {
                background-color: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }

            .error {
                color: red;
                text-align: center;
            }
        </style>
    </head>

    <body>
        <h1>Jokes API</h1>

        <div id="controls">
            <button id="aleatory">Generate</button>
        </div>

        <div class="jokes-container" id="jokesContainer">
        </div>

        <script>
            const jokesContainer = document.getElementById('jokesContainer');
            const button = document.getElementById('aleatory');

            button.addEventListener('click', e => {
                e.preventDefault();
                fetch_aleatory();
            });
            async function fetch_aleatory() {
                console.log("fetching....");
                await fetch("http://127.0.0.1:8000/api/").then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch jokes');
                    }
                    console.log("Request success");
                    return response.json();

                }).then(data => {
                    joke = data['aleatory_joke'];
                    jokesContainer.innerHTML =
                        `
                    <div class="joke">
                        <p>#${joke['id']}</p>
                        <p><b>Pergunta: </b>${joke['ask']}</p>
                        <p><b>Resposta: </b>${joke['response']}</p>
                        <p><b>Categoria: </b>${joke['name']}</p>
                    </div>
                    `;

                });
            }
        </script>

    </body>

    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/api/")
def all_jokes():
    all_jokes = jokes_repository.fetch_all()
    return {"aleatory_joke": all_jokes[randint(0, len(all_jokes))-1],
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