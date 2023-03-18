from pydantic import BaseModel, Field
from typing import Optional, List

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
