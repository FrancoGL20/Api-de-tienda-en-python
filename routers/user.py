from fastapi import APIRouter
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User

user_router=APIRouter()
    
# Ruta para autenticar al usuario
@user_router.post('/login',tags=['auth'],response_model=str,status_code=200)
def login(user:User) -> str:
    if user.email=="admin@gmail.com" and user.password=="admin":
        token:str=create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=401, content="Invalid credentials")
