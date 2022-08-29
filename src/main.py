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
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File


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


class LoginBase(BaseModel):
    username: str = Field(..., max_length=20, example='fede23')
    message: str = Field(default='Login successfull')


class Login(LoginBase):
    password: str = Field(..., min_length=8, example='secretosecreto')


class LoginOut(LoginBase):
    ...

# Path Operator Decoration


@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Home'],
)
async def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200


# Request and Response Body


@app.post(
    path='/persons/',
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons'],
    summary='Create Person in the app',
)
async def add_person(person: Person = Body(...)):  # (...) Obligatorio
    """Create Person

    This path operation created a person in the app and save the information in the database

    Args:

        person: Person -> A person model whith: 
            first_name: Str, min_length=1, max_length=50.
            last name: Str, min_length=1, max_length=50.
            age: Int, min=0, max=115.
            email: Email Type.
            hair color: Str, white, brown, black, blonde, red'
            marital status: Bool

    Returns:

    A person model whith first name, last name, age, email, hair color and marital status  
    """
    return person


# Validations: Query Parameters
# Deprecated
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Show Person in the app',
    deprecated=True,
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
    """Show Person

    Show the person in the app, whit name and age

    Args:

        name (str or optional): min_length=1, max_length=50.
        age (Str Required):

    Returns:

        {
            name: age
        }
    """
    return {name: age}


# Validations: Query Parameters

persons = [1, 2, 3, 4, 5]


@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Show Person by Id in the app',
)
async def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person Id',
        description="This is the person id. It's requered and must be greater than 0",
        example=20,
    )
):
    """Show Person by Id

    Show a person by person_id if exists in the database

    Args:

        person_id (int, optional): not person_id=0.

    Raises:

        HTTPException: status_code=404, This person doesn't exist. 

    Returns:

        {
            person_id: 'It exists'
        }
    """

    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: 'It exists!'}


# Validations: Request Body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Update person in the app',
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
    """Update Person

    Update a person by person_id in the app and update in the database

    Args:

        person_id (int, optional): This is the person id. 
        person (Person, required): This is a person model, content:
            first_name (str) min_length=1, max_length=50.
            last_name (str): min_length=1, max_length=50.
            age: (int): min=0, max=115.
            email (email Type).
            hair color (str):, white, brown, black, blonde, red-
            marital status (bool): (default is false).
        location (Location, required): This is a Location model, content:
            city (str): This is a city,
            state (str): This is a state of the city,
            country (str): This is a country.

    Returns:

        json: a json of the person information.
    """
    # To Dict
    results = person.dict()
    # Combined
    results.update(location.dict())
    return results

# Forms


@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Persons'],
    summary='Login in the app',
)
async def login(username: str = Form(...), password: str = Form(...)):
    """Login

    This path operation login in the app

    Args:

        username (str, required): This is the username.
        password (str, required): This is the password, min 8 characters.

    Returns:

        json: a json of strings representing the user 
    """
    return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contact'],
    summary='Form contact in the app',
)
async def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Yvan'
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example='Varela'
    ),
    email: EmailStr = Form(..., example='email@example.com'),
    message: str = Form(
        ...,
        min_length=20,
        example='FastApi is amazing, but a need more learnig'
    ),
    user_agent: str | None = Header(default=None),
    ads: str | None = Cookie(default=None)
):
    """Form Contact

    This path operation post a Form contact in the app and save in the database

    Args:

        first_name (str, required): This is the first name, minimum characters is 1 and maximum is 20.
        last_name (str, required): This is the last name, minimum characters is 1 and maximum is 20.
        email (EmailStr, required): This is the email.
        message (str, required): This is a the contact message and minimum characters is 20.
        user_agent (str, optional): This is a contact headers.
        ads (str, optional): This is a contact cookies.

    Returns:

        string: a string content the user agent information
    """
    return user_agent


# Files

@app.post(
    path='/image',
    tags=['Upload Files'],
    summary='Upload image in the app',
)
async def post_image(
    image: UploadFile = File(...)
):
    """Upload Image

    The path operation upload a image in the app and save in the database

    Args:

        image (UploadFile, required): This is the image.

    Returns:

        json: a json that contains the information of the image
    """

    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read())/1024, ndigits=2)
    }


# Multiples images

@app.post(
    path='/image-multiple',
    tags=['Upload Files'],
    summary='Upload image in the app',
)
async def post_image_multiple(
    images: list[UploadFile] = File(...)
):
    """Upload Images

    The route operation upload the images into the application and saves them to the database

    Args:

        images (list[UploadFile], required): This is a list of images.

    Returns:

        list: a list of json that contains the information of the images
    """

    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    } for image in images]

    return info_images
