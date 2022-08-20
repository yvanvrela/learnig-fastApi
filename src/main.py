from fastapi import FastAPI

# Instancia de la clase
app = FastAPI()


# Path Operator Decoration
@app.get('/')
def home() -> dict:
    # return JSON
    return {'hello': 'word'}, 200
