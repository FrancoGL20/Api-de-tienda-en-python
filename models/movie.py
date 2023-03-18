from config.database import Base  # Importamos la clase base para los modelos
# Se importan los tipos de datos de la base de datos y las columnas de la tabla
from sqlalchemy import Column, Integer, String, Float # Importamos los tipos de datos de la base de datos y las columnas de la tabla

class Movie(Base):
    __tablename__ = "movies"  # Nombre de la tabla en la base de datos
    
    # Se definen las columnas de la tabla en la base de datos y sus tipos de datos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
