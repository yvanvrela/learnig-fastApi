# Python
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastApi
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path

# Instancia de la clase
app = FastAPI()


# Models

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example='Enc'
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example='Itapua'
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example='Paraguay'
    )

# Enum create numerate strings
# Use to specific cases


class HairColr(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

# Validate atributes whith Field class


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    email: EmailStr
    # Recieved HairColor class
    hair_color: HairColr | None = Field(default=None)
    is_married: bool | None = Field(default=None)

    # Schema
    class Config:
        schema_extra = {
            'example': {
                'first_name': 'Yvan',
                'last_name': 'Varela',
                'age': '23',
                'hair_color': 'brown',
                'is_married': False
            }
        }


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


# Validations: Query Parameters

@app.get('/person/detail')
async def show_person(
    name: str | None = Query(
        default=None,
        min_length=1, max_length=50,
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters"
    ),
    age: str = Query(
        ...,  # Not recomender but is a option
        title='Person Age',
        description="This is the person age. It's required"
    )
):
    return {name: age}


# Validations: Query Parameters

@app.get('/person/detail/{person_id}')
async def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person Id',
        description="This is the person id. It's requered and must be greater than 0"
    )
):
    return {person_id: 'It exists!'}


# Validations: Request Body

@app.put('/person/{person_id}')
async def update_person(
    person_id: int = Path(
        ...,
        title='Person Id',
        description="This is the person id",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    # To Dict
    results = person.dict()
    # Combined
    results.update(location.dict())
    return results
