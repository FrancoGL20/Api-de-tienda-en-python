from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import create_token, validate_token

# Clase para autenticar al usuario con token
class JWTBearer(HTTPBearer):
    async def __call__(self, request:Request): # request: objeto que contiene la información de la petición
        aut= await super().__call__(request) # Se obtiene el token de la petición HTTP
        data=validate_token(aut.credentials) # Se valida el token
        if data['email'] != "admin@gmail.com" and data['password'] != "admin": # Se valida el usuario y contraseña
            raise HTTPException(status_code=403,detail="Invalid credentials") # Se lanza una excepción si el usuario o contraseña son incorrectos