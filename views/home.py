home_content = """
<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jokes API Frontend</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      background-color: #2e2e2e;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 96vh;
    }

    h1,
    h2 {
      text-align: center;
      color: #ffffff;
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

    .main {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    select {
      padding: 10px;
      font-size: 16px;
    }
  </style>
</head>

<body>
  <div class="main">
    <h1>Jokes API</h1>
    <select name="type" id="select">
      <option value="aleatory">aleatório</option>
      <option value="category">Cateogoria</option>
      <option value="all">Todas (limite - 10)</option>
    </select>
  </div>

  <div id="controls">
    <button id="get">Generate</button>
  </div>
  <div class="jokes-container" id="jokesContainer">

  </div>

  <script>
    const jokesContainer = document.getElementById('jokesContainer');
    const button = document.getElementById('get');
    const select = document.getElementById('select');
    const main = document.querySelector('.main');
    const controls = document.getElementById('controls');

    function addButtonListener() {
      const button = document.getElementById('get');
      if (button) {
        button.addEventListener('click', e => {
          startRequest();
        });
      }

      document.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
          startRequest();
        }
      });

      function startRequest() {
        console.log(select.value);
        if (select.value == "aleatory") {
          fetch_aleatory();
        } else if (select.value == "category") {
          fetch_category();
        } else {
          fetch_all();
        }
      }
    }


    select.addEventListener('change', e => {
      if (select.value == "category") {
        controls.innerHTML = "<input type='text' id='category' placeholder='Digite a categoria'>" + controls.innerHTML;
      } else {
        controls.innerHTML = "<button id='get'>Generate</button>";
      }
      addButtonListener();
    });
    addButtonListener();


    async function fetch_aleatory() {
      console.log("fetching....");
      await fetch(`https://badjokesapi.vercel.app/api/`).then(response => {

        //await fetch("https://badjokesapi.vercel.app/api/").then(response => {
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

    async function fetch_category() {
      const category = document.getElementById('category').value;
      console.log(category);
      if (category !== undefined && category !== null && category !== "") {
        console.log("fetching....");
        //await fetch(`http://127.0.0.1:8000/api/jokes/c/category?category=${category}`).then(response => {
        await fetch(`https://badjokesapi.vercel.app/api/jokes/c/category?category=${category}`).then(response => {
          if (!response.ok) {
            throw new Error('Failed to fetch jokes');
          }
          console.log("Request success");
          return response.json();

        }).then(data => {
          if (data['error']) {
            jokesContainer.innerHTML = "<p class='error'>Nenhuma piada encontrada com essa categoria</p>";
            return;
          }
          jokes = data['jokes'];
          jokesContainer.innerHTML = '';
          jokes.forEach(joke => {
            jokesContainer.innerHTML +=
              `
                    <div class="joke">
                        <p>#${joke['id']}</p>
                        <p><b>Pergunta: </b>${joke['ask']}</p>
                        <p><b>Resposta: </b>${joke['response']}</p>
                        <p><b>Categoria: </b>${joke['name']}</p>
                    </div>
                    `;
          });


        }).catch(error => {
          console.log(error);
        });
      } else {
        alert("Digite uma categoria");
      }

    }
    async function fetch_all() {
      console.log("fetching....");
      //await fetch("http://127.0.0.1:8000/api/jokes").then(response => {
      await fetch("https://badjokesapi.vercel.app/api/jokes/").then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch jokes');
        }
        console.log("Request success");
        return response.json();
      }).then(data => {
        jokes = data['jokes'];
        console.log(jokes);
        jokesContainer.innerHTML = '';
        jokes.forEach(joke => {
          jokesContainer.innerHTML +=
            `
              <div class="joke">
                  <p>#${joke['id']}</p>
                  <p><b>Pergunta: </b>${joke['ask']}</p>
                  <p><b>Resposta: </b>${joke['response']}</p>
                  <p><b>Categoria: </b>${joke['name']}</p>
              </div>
            `;
        });
      });
    }

  </script>

</body>

</html>
"""