# API de tienda

## Descripción
El proyecto consta de una api documentada con un CRUD de peliculas, esta api tiene unicamente datos de prueba, no se conecta a ninguna base de datos, es solo para probar el funcionamiento de la misma y la documentación.

## Instalación
Para instalar el proyecto se debe clonar el repositorio como primer paso. Una vez clonado el repositorio se deben seguir los siguientes pasos:
1. Crear un entorno virtual
    ```sh
    python -m venv env
    ```
2. Activar el entorno virtual
    
    Para Windows:
    ```sh
    env\Scripts\activate
    ```

    Para Linux:
    ```sh
    source env/bin/activate
    ```

3. Instalar las dependencias
    ```sh
    pip install -r requirements.txt
    ```

## Ejecución
Para ejecutar el proyecto se ejecuta el siguiente comando:
```sh
uvicorn main:app --reload
```
Esto iniciará el servidor en el puerto 8000.

Para acceder a la documentación de la api se debe ingresar a la siguiente url:
```sh
http://localhost:8000/docs
```

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)