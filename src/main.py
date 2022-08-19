from fastapi import FastAPI

# Instancia de la clase
app = FastAPI()


# Path Operator Decoration
@app.get('/')
def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200


"""
    # Path Operations
    Un path va despues del dominio -> mi-dominio.com/PATH/
    Path -> Routes -> Endpoints     mi-dominio.com/API/

    # Operations
    Devuelve un header adicional llamado allow que contiene los metodos 
    http que se utiliza en los endpoints.
"""
