from pydantic import BaseModel

class CreateFilm(BaseModel):
    title: str
    author: str