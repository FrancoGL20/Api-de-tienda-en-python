# Para crear un middleware
from starlette.middleware.base import BaseHTTPMiddleware 
# Para recibir la petición y retornar la respuesta
from fastapi import FastAPI, Request, Response 
# Para retornar una respuesta en formato JSON
from fastapi.responses import JSONResponse 

# Middleware para manejar los errores de la aplicación de forma global en todas las rutas
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # Función que se ejecuta cuando se produce un error en la aplicación
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        # Se intenta ejecutar la petición
        try:
            return await call_next(request)
        # Si se produce un error se retorna un mensaje de error en formato JSON
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})