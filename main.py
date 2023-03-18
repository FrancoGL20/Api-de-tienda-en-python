from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse # Para poder usar respuestas en HTML y JSON
from pydantic import BaseModel # Para poder usar modelos de datos
from fastapi.security import HTTPBearer # Para poder usar autenticación por token
from jwt_manager import create_token,validate_token # Importar funciones para crear y validar token
from config.database import engine, Base # Para poder usar la base de datos
from middlewares.error_handler import ErrorHandler # Importar el middleware para manejar los errores
from routers.movie import movie_router # Importar el router de la API

# Caracteristicas de la API en la documentación
app = FastAPI() # Crear una instancia de FastAPI
app.title = "My First API" # Titulo de la API
app.version = "0.0.1" # Version de la API

# Agregar el middleware para manejar los errores
app.add_middleware(ErrorHandler) 

# Agregar el router de la API
app.include_router(movie_router) 

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine) 


class User(BaseModel):
    email:str
    password:str

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

