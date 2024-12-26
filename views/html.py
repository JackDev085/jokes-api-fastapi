import os 

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


with open(f"{ROOT_PATH}/html/index.html", "r",encoding="utf8") as file:
    home_content = file.read()

with open(f"{ROOT_PATH}/html/create.html", "r",encoding="utf8") as file:
    create_content = file.read()

with open(f"{ROOT_PATH}/html/update.html", "r",encoding="utf8") as file:
    update_content = file.read()