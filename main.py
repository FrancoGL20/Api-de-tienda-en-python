from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse # Para poder usar respuestas en HTML y JSON
from pydantic import BaseModel # Para poder usar modelos de datos
from fastapi.security import HTTPBearer # Para poder usar autenticación por token
from utils.jwt_manager import create_token,validate_token # Importar funciones para crear y validar token
from config.database import engine, Base # Para poder usar la base de datos
from middlewares.error_handler import ErrorHandler # Importar el middleware para manejar los errores
from routers.movie import movie_router # Importar el router de peliculas
from routers.user import user_router # Importar el router de usuarios

# Caracteristicas de la API en la documentación
app = FastAPI() # Crear una instancia de FastAPI
app.title = "My First API" # Titulo de la API
app.version = "0.0.1" # Version de la API

# Agregar el middleware para manejar los errores
app.add_middleware(ErrorHandler) 

# Agregar los routers a la API
app.include_router(movie_router) 
app.include_router(user_router)


# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine) 

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

# Ruta de inicio de la API
@app.get("/",tags=['home'])
def message():
    return HTMLResponse('<h1>My First API</h1>') # Respuesta en HTML
