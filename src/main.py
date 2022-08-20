# Pydantic
from pydantic import BaseModel

# FastApi
from fastapi import FastAPI
from fastapi import Body

# Instancia de la clase
app = FastAPI()


# Models


class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: str | None = None  # Optional
    is_married: bool | None = None  # Optional


# Path Operator Decoration


@app.get('/')
async def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200


# Request and Response Body


@app.post('/person/')
async def add_person(person: Person = Body(...)):
    return person
