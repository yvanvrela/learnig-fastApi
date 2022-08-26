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


# Fake Data

fake_persons = [
    {
        'first_name': 'Fede',
        'last_name': 'Varela',
        'age': 22,
        'hair_color': None,
        'is_married': False,
    },
    {
        'first_name': 'Aldo',
        'last_name': 'Bala',
        'age': 50,
        'hair_color': 'Red',
        'is_married': True,
    },
]


# Path Operator Decoration


@app.get('/')
async def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200


# Request and Response Body


@app.post('/persons/')
async def add_person(person: Person = Body(...)):  # (...) Obligatorio
    return person
