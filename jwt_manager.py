from jwt import encode, decode
from dotenv import load_dotenv # Cargar variables de entorno
import os # Para acceder a las variables de entorno

load_dotenv() # Cargar variables de entorno

def create_token(user:dict):
    token:str=encode(payload=user,key=os.getenv("TOKEN_KEY"),algorithm="HS256") # payload: datos que se van a encriptar, key: clave secreta, algorithm: algoritmo de encriptación
    return token

def validate_token(token:str) ->dict:
    data:dict=decode(token,key=os.getenv("TOKEN_KEY"),algorithms=["HS256"]) # key: clave secreta, algorithms: algoritmo de desencriptación
    return data