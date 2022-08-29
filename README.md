# Learnig FastApi

### Requirements

- fastapi
- uvicorn

### Run Server

`uvicorn main:app --reload`

---

### Path Operations

Un path va despues del dominio --> mi-dominio.com/PATH/

Path --> Routes --> Endpoints mi-dominio.com/API/

```python
@app.get('/')
    async def home() -> dict:
        # return JSON
        return {'hello': 'word'}, 200
```

#### Operations

Devuelve un header adicional llamado allow que contiene los metodos
http que se utiliza en los endpoints

#### Path Parameter

Los parametros de rutas son parte variable de un URL se utiliza para señalar un recurso especifico de una coleccion por ej por su id en python deben estar dentro de llaves **"{parameter}"**

**Pasarlo es obligatorio**
/path/{id}

---

### Request Body - Response Body

Cuando el cliente se cominica con el servidor se denomina Request y cuanto es al reves se denomina Response.

Request Body es el **body** de una **peticion** http

Response Body es la **respuesta** de una **peticion** http

Los dos se envian en formato JSON

---

#### Query Parameters

Es un conjunto de elementos opcionales que se añaden al finalizar la ruta con el objetivo de definir contenido o acciones a la url.

Lo ideal es que siempre sea opcional.

Se añaden despues de "?" y para agregar mas se utiliza "&".

GET --> /users/{user_id}/details
PUT --> /users/{user_id}/details?age=20
PUT --> /users/{user_id}/details?age=20&height=180

---

#### Validation Query

Opcional para el nombre se define como un str, y la validacion se hace con un parametro.
Query que es una clase de FastApi.

**Str:**

- **min_length:**
- **max_length:**
- **regex:**

**Int:**

- **ge:** Greater or equal than --> (>=)
- **le:** Less or rqual than --> (<=)
- **gt:** Grater than --> (>)
- **lt:** Less than --> (<)

**Documentation query parameters:**
Para una mejor documentacion de los query.

- **Title:**
- **description:**

---

#### Datos especiales

Pydantic Types
For more information, see the [Field Types Pydantic](https://pydantic-docs.helpmanual.io/usage/types/ "Field Types Pydantic")
Exotics - Common

- **Enum:**
- **HttpUrl:** Validate url.
- **FilePath:** Validate route. --> C:/windows/system32/400.dll
- **DirectorPath:** Validate route. --> /C/windows/system32/
- **EmailStr:** Validate email --> hi@hi.com
- **PaymentCardNumber:**
- **IPvAnyAddress:**
- **PositiveFloat:**
- **NegativeFloat:**
- **PositiveInt:**
- **NegativeInt:**

---

### Cookie

Una pieza de codigo que un servidor mete en tu computadora cuando estas navegando en la web.

### Headers

Una parte de una peticion o respuesta HTTP que contiene datos sobre la peticion o la respuesta como el formato, quien la hizo, el contendio, etc.

---

### Data input types

- Path Parameters --> URL (obligatorios)
- Query Parameters --> URL (opcionales)
- Request Body --> JSON
- Forms --> Campos del frondtend
- Headers --> cabeceras HTTP
- Cookies --> Almacena informacion
- Files
  - File
  - Upload File
    - Filename
    - Content_type --> File format
    - File --> El archivo en si mismo
