from fastapi import Path,Query,Depends
from fastapi.responses import JSONResponse # Para poder retornar respuestas en formato JSON
from fastapi.encoders import jsonable_encoder # Para poder usar el método jsonable_encoder
from pydantic import BaseModel, Field # Para poder usar modelos de datos y validaciones
from typing import Optional,List # Para poder usar tipos de datos opcionales y listas
from fastapi.security import HTTPBearer # Para poder usar autenticación por token
from config.database import Session # Para poder usar la sesión con la base de datos
from models.movie import Movie as MovieModel # Importar el modelo de datos de la tabla movies
from middlewares.jwt_bearer import JWTBearer # Importar el middleware para manejar la autenticación por token
from fastapi import APIRouter, Depends, HTTPException # Para poder usar rutas, dependencias y excepciones

# Crear una instancia de la clase APIRouter para poder crear rutas dentro de un router
movie_router=APIRouter()

# Esquema de datos para las películas
class Movie(BaseModel): 
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
                "title":"Mí película",
                "overview":"Descripción de la película",
                "year":2021,
                "rating":9.8,
                "category":"Acción"
            }
        }


# Ruta para obtener todas las películas
@movie_router.get('/movies',tags=['movies'],response_model=List[Movie],status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    # Crear una sesión con la base de datos
    db:Session=Session() 
    # Obtener todos los registros de la tabla movies
    result=db.query(MovieModel).all() 
    # Cerrar la sesión con la base de datos
    db.close() 
    
    # Respuesta con los registros de la tabla movies en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

#------------------------------------------------------#
# ---------------  Parametros de ruta ---------------- #
#------------------------------------------------------#

@movie_router.get('/movies/{movie_id}',tags=['movies'],response_model=Movie)
def get_movie(movie_id:int=Path(ge=1,le=2000)) -> Movie:
    # Crear una sesión con la base de datos
    db:Session=Session()
    # Obtener el registro de la tabla movies con el id indicado
    result=db.query(MovieModel).filter(MovieModel.id==movie_id).first() 
    # Cerrar la sesión con la base de datos
    db.close() 
    
    # Si no se encuentra el registro se retorna un mensaje de error
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Respuesta con el registro de la tabla movies en formato JSON
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) 

#-------------------------------------------------------#
# ---------------  Parametros de query ---------------- #
#-------------------------------------------------------#

@movie_router.get("/movies/",tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category:str=Query(min_length=5,max_length=15)) -> List[Movie]:
    # Crear una sesión con la base de datos
    db:Session=Session() 
    # Obtener los registros de la tabla movies con la categoría indicada
    result=db.query(MovieModel).filter(MovieModel.category==category).all() 
    # Cerrar la sesión con la base de datos
    db.close() 
    
    if not result:
        return JSONResponse(content={"message":"Movies not found"},status_code=404)
    
    # Respuesta con los registros de la tabla movies en formato JSON
    return JSONResponse(status_code=404, content=jsonable_encoder(result)) 

#-------------------------------------------------------#
# --------------- Metodo POST ------------------------- #
#-------------------------------------------------------#

@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie:Movie) -> dict:
    db=Session() # Crear una sesión con la base de datos
    new_movie=MovieModel(**movie.dict()) # Crear un objeto de tipo MovieModel
    db.add(new_movie) # Agregar el objeto a los cambios pendientes
    db.commit() # Guardar los cambios en la base de datos
    db.close() # Cerrar la sesión con la base de datos
    return JSONResponse(status_code=201, content={'message':'Movie created successfully'})

# ------------------------------------------------------#
# --------------- Metodo PUT -------------------------- #
# ------------------------------------------------------#

@movie_router.put('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(movie_id:int,movie:Movie) -> dict:
    # Crear una sesión con la base de datos
    db:Session=Session()
    # Obtener el registro de la tabla movies con el id indicado
    result=db.query(MovieModel).filter(MovieModel.id==movie_id).first()
    
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Actualizar los valores del registro
    result.title=movie.title
    result.overview=movie.overview
    result.year=movie.year
    result.rating=movie.rating
    result.category=movie.category
    
    # Guardar los cambios en la base de datos
    db.commit()
    # Cerrar la sesión con la base de datos
    db.close()
    
    return JSONResponse(status_code=200, content={'message':'Movie updated successfully'})


# ------------------------------------------------------#
# --------------- Metodo DELETE ----------------------- #
# ------------------------------------------------------#

@movie_router.delete('/movies/{movie_id}',tags=['movies'],response_model=dict,status_code=200)
def delete_movie(movie_id:int) -> dict:
    # Crear una sesión con la base de datos
    db:Session=Session()
    # Obtener el registro de la tabla movies con el id indicado
    result=db.query(MovieModel).filter(MovieModel.id==movie_id).first()
    
    if not result:
        return JSONResponse(content={"message":"Movie not found"},status_code=404)
    
    # Eliminar el registro de la base de datos
    db.delete(result) 
    # Guardar los cambios en la base de datos
    db.commit()
    # Cerrar la sesión con la base de datos
    db.close()
    
    return JSONResponse(status_code=404, content={'message':'Movie deleted successfully'})
