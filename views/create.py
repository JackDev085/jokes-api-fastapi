create_content = """
<!DOCTYPE html>
<html>

<head>
  <meta charset='utf-8'>
  <meta http-equiv='X-UA-Compatible' content='IE=edge'>
  <title>Page Title</title>
  <meta name='viewport' content='width=device-width, initial-scale=1'>

  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 0;
    }

    .create_joke {
      width: 300px;
      margin: 50px auto;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
    }

    .create_joke h1 {
      text-align: center;
      color: #333;
    }

    .create_joke label {
      display: block;
      margin-bottom: 5px;
      color: #333;
    }

    .create_joke input {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }

    .create_joke button {
      width: 100%;
      padding: 10px;
      background-color: #28a745;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    .create_joke button:hover {
      background-color: #218838;
    }
  </style>
</head>

<body>
  <div class="create_joke">
    <h1>Create a Joke</h1>
    <form action="https://badjokesapi/api/jokes/create/" method="post" enctype="application/json">
      <label for="ask">Pergunta</label>
      <input type="text" id="ask" name="ask" required>
      <label for="response">Resposta</label>
      <input type="text" id="response" name="response" required>
      <label for="category_id">Categoria</label>
      <input type="int" id="category_id" name="category_id" required>
      <button id="submit" type="submit">Criar</button>

    </form>

  </div>
</body>
<script>
  const form = document.querySelector("form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ask = document.querySelector("#ask").value;
    const response = document.querySelector("#response").value;
    const category_id = document.querySelector("#category_id").value;

    await fetch("https://badjokesapi/api/jokes/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        ask,
        response,
        category_id,
      }),
    }).then((response) => {
      if (response.ok) {
        alert("Joke created successfully");
      }
    });
  });

</script>

</html>
"""