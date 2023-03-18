import os # Permite acceder a las rutas del sistema operativo
from sqlalchemy import create_engine # Permite crear la conexión con la base de datos
from sqlalchemy.orm.session import sessionmaker # Permite crear la sesión con la base de datos
from sqlalchemy.ext.declarative import declarative_base # Permite crear la clase base para los modelos


# Nombre del archivo de la base de datos
sqlite_file_name="../database.sqlite" 
# Ruta del archivo actual
base_dir = os.path.dirname(os.path.realpath(__file__))

# Ruta de la base de datos
database_url=f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}" 

# Se crea la conexión con la base de datos
engine=create_engine(database_url,echo=True) 

# Se crea la sesión con la base de datos
Session=sessionmaker(bind=engine)

# Se crea la clase base para los modelos
Base=declarative_base()