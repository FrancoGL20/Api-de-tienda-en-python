from fastapi import Path,Query,Depends
from fastapi.responses import JSONResponse # Para poder retornar respuestas en formato JSON
from fastapi.encoders import jsonable_encoder # Para poder usar el método jsonable_encoder
from pydantic import BaseModel, Field # Para poder usar modelos de datos y validaciones
from typing import Optional,List # Para poder usar tipos de datos opcionales y listas
from fastapi.security import HTTPBearer # Para poder usar autenticación por token
from config.database import Session # Para poder usar la sesión con la base de datos
from middlewares.jwt_bearer import JWTBearer # Importar el middleware para manejar la autenticación por token
from fastapi import APIRouter, Depends, HTTPException # Para poder usar rutas, dependencias y excepciones
from models.movie import Movie as MovieModel # Importar el modelo de datos de la tabla movies
from services.movie import MovieService # Importar el servicio para manejar las operaciones de la tabla movies
from schemas.movie import Movie # Importar el esquema de datos para las películas

# Crear una instancia de la clase APIRouter para poder crear rutas dentro de un router
movie_router=APIRouter()


# Ruta para obtener todas las películas
@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies() -> List[Movie]:
    # Obtener todos los registros de la tabla movies
    result=MovieService().get_movies()
    # Respuesta con los registros de la tabla movies en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 


# Ruta para consultar una película por id
@movie_router.get('/movies/{movie_id}',tags=['movies'],response_model=Movie)
def get_movie(movie_id:int=Path(ge=1,le=2000)) -> Movie:
    # Obtener el registro de la tabla movies con el id indicado
    result=MovieService().get_movie(movie_id)
    
    # Si no se encuentra el registro se retorna un mensaje de error
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Respuesta con el registro de la tabla movies en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 


# Ruta para obtener las películas por categoría
@movie_router.get("/movies/",tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
    # Obtener los registros de la tabla movies con la categoría indicada
    result=MovieService().get_movies_by_categoy(category)
    
    if not result:
        return JSONResponse(content={"message":"Movies not found"},status_code=404)
    
    # Respuesta con los registros de la tabla movies en formato JSON
    return JSONResponse(status_code=404, content=jsonable_encoder(result)) 


# Ruta para crear una película
@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    MovieService().create_movie(movie)
    return JSONResponse(status_code=201, content={'message':'Movie created successfully'})


# Ruta para actualizar una película
@movie_router.put('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(movie_id:int,movie:Movie) -> dict:
    # Obtener el registro de la tabla movies con el id indicado
    result=MovieService().get_movie(movie_id)
    
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Actualizar los valores del registro
    MovieService().update_movie(movie_id,movie)
    
    return JSONResponse(status_code=200, content={'message':'Movie updated successfully'})


# Ruta para eliminar una película
@movie_router.delete('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(movie_id:int) -> dict:
    # Obtener el registro de la tabla movies con el id indicado
    result=MovieService().get_movie(movie_id)
    
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Eliminar el registro de la tabla movies
    MovieService().delete_movie(movie_id)
    
    return JSONResponse(status_code=404, content={'message':'Movie deleted successfully'})
