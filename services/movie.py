# Modelo de la tabla movies
from models.movie import Movie as MovieModel
# Clase para crear una sesión con la base de datos
from config.database import Session
from schemas.movie import Movie

class MovieService():
    def __init__(self):
        pass
    
    # Función para obtener todos los registros de la tabla movies
    def get_movies(self):
        db:Session=Session() 
        # Obtener todos los registros de la tabla movies
        result=db.query(MovieModel).all()
        db.close() 
        return result
    
    # Función para obtener un registro de la tabla movies
    def get_movie(self,id:int):
        db:Session=Session() 
        # Obtener el registro de la tabla movies con el id indicado
        result=db.query(MovieModel).filter(MovieModel.id==id).first()
        db.close() 
        return result

    # Función para obtener las películas de una categoría
    def get_movies_by_categoy(self,categoria:str):
        db:Session=Session() 
        # Obtener el registro de la tabla movies con el id indicado
        result=db.query(MovieModel).filter(MovieModel.category==categoria)
        db.close() 
        return result
    
    def create_movie(self,movie:Movie):
        db:Session=Session() 
        # Crear un nuevo registro en la tabla movies con los datos del objeto movie
        new_movie=MovieModel(**movie.dict())
        db.add(new_movie)
        db.commit()
        db.close()
        return
    
    def update_movie(self,id:int,movie:Movie):
        db:Session=Session() 
        # Obtener el registro de la tabla movies con el id indicado
        result=db.query(MovieModel).filter(MovieModel.id==id).first()
        result.title=movie.title
        result.overview=movie.overview
        result.year=movie.year
        result.rating=movie.rating
        result.category=movie.category
        db.commit()
        db.close()
        return
    
    def delete_movie(self,id:int):
        db:Session=Session() 
        # Obtener el registro de la tabla movies con el id indicado
        result=db.query(MovieModel).filter(MovieModel.id==id).first()
        db.delete(result)
        db.commit()
        db.close()
        return