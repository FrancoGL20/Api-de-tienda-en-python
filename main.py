from fastapi import FastAPI,Body,Path,Query,Request,Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse # Para poder usar respuestas en HTML y JSON
from pydantic import BaseModel, Field # Para poder usar modelos de datos y validaciones
from typing import Optional,List # Para poder usar tipos de datos opcionales y listas
from fastapi.security import HTTPBearer # Para poder usar autenticación por token
from jwt_manager import create_token,validate_token # Importar funciones para crear y validar token

app = FastAPI() # Crear una instancia de FastAPI
app.title = "My First API" # Titulo de la API
app.version = "0.0.1" # Version de la API

# Clase para autenticar al usuario con token
class JWTBearer(HTTPBearer):
    async def __call__(self, request:Request): # request: objeto que contiene la información de la petición
        aut= await super().__call__(request) # Se obtiene el token de la petición HTTP
        data=validate_token(aut.credentials) # Se valida el token
        if data['email'] != "admin@gmail.com" and data['password'] != "admin": # Se valida el usuario y contraseña
            raise HTTPException(status_code=403,detail="Invalid credentials") # Se lanza una excepción si el usuario o contraseña son incorrectos

class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel): # Crear un esquema de datos para la API
    id:Optional[int]=None # id de tipo entero y opcional con valor por defecto None
    title:str=Field(min_length=5,max_length=15)
    overview:str=Field(min_length=15,max_length=50)
    year:int=Field(gt=1900,le=2022) # gt: mayor que, le: menor o igual que
    rating:float=Field(ge=0.0,le=10.0)
    category:str=Field(min_length=3,max_length=20)
    
    # método para mostrar un ejemplo de los datos que se deben enviar
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"Mí película",
                "overview":"Descripción de la película",
                "year":2021,
                "rating":9.8,
                "category":"Acción"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },{
        'id': 2,
        'title': 'Titanic',
        'overview': "Un joven millonario se enamora de una joven de clase ...",
        'year': '1997',
        'rating': 7.8,
        'category': 'Drama'
    }
]

#------------------------------------------------------#
# ---------------  Rutas de la API ------------------- #
# -----------------------------------------------------#

# Ruta de inicio
@app.get("/",tags=['home'])
def message():
    return HTMLResponse('<h1>My First API</h1>') # Respuesta en HTML

# Ruta para autenticar al usuario
@app.post('/login',tags=['auth'],response_model=str,status_code=200)
def login(user:User) -> str:
    if user.email=="admin@gmail.com" and user.password=="admin":
        token:str=create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=401, content="Invalid credentials")

# Ruta para obtener todas las películas
@app.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies) # Respuesta en JSON

#------------------------------------------------------#
# ---------------  Parametros de ruta ---------------- #
#------------------------------------------------------#

@app.get('/movies/{movie_id}',tags=['movies'],response_model=Movie)
def get_movie(movie_id:int=Path(ge=1,le=2000)) -> Movie:
    for item in movies:
        if item['id'] == movie_id:
            return JSONResponse(status_code=200, content=item)
    
    return JSONResponse(status_code=404, content=[])

#-------------------------------------------------------#
# ---------------  Parametros de query ---------------- #
#-------------------------------------------------------#

@app.get("/movies/",tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
    for item in movies:
        if item['category'] == category:
            return JSONResponse(status_code=200, content=item)
    
    return JSONResponse(status_code=404, content=[])

#-------------------------------------------------------#
# --------------- Metodo POST ------------------------- #
#-------------------------------------------------------#

@app.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={'message':'Movie created successfully'})

# ------------------------------------------------------#
# --------------- Metodo PUT -------------------------- #
# ------------------------------------------------------#

@app.put('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(movie_id:int,movie:Movie) -> dict:
    for item in movies:
        if item["id"]==movie_id:
            item["title"]=movie.title
            item["overview"]=movie.overview
            item["year"]=movie.year
            item["rating"]=movie.rating
            item["category"]=movie.category
            return JSONResponse(status_code=200, content={'message':'Movie updated successfully'})
    
    return JSONResponse(status_code=404, content=[])

# ------------------------------------------------------#
# --------------- Metodo DELETE ----------------------- #
# ------------------------------------------------------#

@app.delete('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200) # Parámetro de tipo path o de ruta
def delete_movie(movie_id:int) -> dict:
    for item in movies:
        if item["id"]==movie_id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={'message':'Movie deleted successfully'})
    
    return JSONResponse(status_code=404, content=[])
