from pydantic import BaseModel

class Joke(BaseModel):
    ask:str
    response:str | None = None
    category_id:int