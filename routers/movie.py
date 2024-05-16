from fastapi import APIRouter
from fastapi import Path, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=list[Movie], status_code=200, dependencies=[Depends(JWTBearer())]) # presenta todas las películas
def get_movies() -> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies']) # muestra la película por su id
def get_movie(id:int = Path(ge=1, le=200)):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Elemento no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies']) # muestra las películas de una categoría
def get_movies_by_category(category:str):
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "Ningún elemento encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies/createmovie', tags=['movies'], response_model=dict, status_code=201) # agrega una nueva película al diccionario
def create_movie(movie:Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Se registró la película"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200) # actualiza/modifica los datos de una película
def update_movie(id:int, movie:Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No se encontró el elemento"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se modificó la película"})
        
@movie_router.delete('/movies/{id}', tags=['movies']) # elimina una película del diccionario
def delete_movie(id:int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message': "No se encontró el elemento"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message': "Se ha borrado el elemento"})