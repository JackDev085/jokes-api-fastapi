from pydantic import BaseModel

class Joke(BaseModel):
    ask:str
    response:str
    category_id:int