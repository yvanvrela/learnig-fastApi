# Learnig FastApi

### Path Operations

Un path va despues del dominio -> mi-dominio.com/PATH/
Path -> Routes -> Endpoints mi-dominio.com/API/

### Operations

Devuelve un header adicional llamado allow que contiene los metodos
http que se utiliza en los endpoints

### Path Parameter

Los parametros de rutas son parte variable de un URL se utiliza para señalar un recurso especifico de una coleccion por ej por su id
en python deben estar dentro de llaves "{parameter}}"
Pasarlo es obligatorio
"/path/{id}"

#### Query Parameters

Esun conjunto de elementos opcionales que se añaden al finalizar la ruta con el objetivo de definir contenido o acciones a la url.
Se añaden despues de "?" y para agregar mas se utiliza "&"
GET -> /users/{user_id}/details
PUT -> /users/{user_id}/details?age=20
PUT -> /users/{user_id}/details?age=20&height=180
