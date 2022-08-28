# Python
from enum import Enum

# Pydantic
# Sirve para definir los modelos de datos
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastApi
# Sirve para definir el tipo de dato
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query
from fastapi import Path
from fastapi import status

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


class HairColr(str, Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

# Validate atributes whith Field class


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Yvan',
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Varela',
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example='23',
    )
    email: EmailStr
    # Recieved HairColor class
    hair_color: HairColr | None = Field(
        default=None,
        example='brown',
    )
    is_married: bool | None = Field(
        default=None,
        example=False,
    )

    # Schema

    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Yvan',
    #             'last_name': 'Varela',
    #             'age': '23',
    #             'hair_color': 'brown',
    #             'is_married': False,
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length=8, example='secretosecreto')


class PersonOut(PersonBase):
    ...


# Path Operator Decoration


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
async def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200


# Request and Response Body


@app.post(
    path='/persons/',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_person(person: Person = Body(...)):  # (...) Obligatorio
    return person


# Validations: Query Parameters

@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
)
async def show_person(
    name: str | None = Query(
        default=None,
        min_length=1, max_length=50,
        title='Person Name',
        description="This is the person name. It's between 1 and 50 characters",
        example='Facundo'
    ),
    age: str = Query(
        ...,  # Not recomender but is a option
        title='Person Age',
        description="This is the person age. It's required",
        example='25'
    )
):
    return {name: age}


# Validations: Query Parameters

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
)
async def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person Id',
        description="This is the person id. It's requered and must be greater than 0",
        example=20
    )
):
    return {person_id: 'It exists!'}


# Validations: Request Body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK,
)
async def update_person(
    person_id: int = Path(
        ...,
        title='Person Id',
        description="This is the person id",
        gt=0,
        example=20
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    # To Dict
    results = person.dict()
    # Combined
    results.update(location.dict())
    return results
