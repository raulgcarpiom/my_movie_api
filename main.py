from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "FastAPI App"
app.version = "1.0"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

# movies = [
#     {
#         "id": 1,
#         "title": "Avatar",
#         "overview": "Aventuras de ciencia ficción sobre alienígenas",
#         "year": "2009",
#         "rating": 7.8,
#         "category": "Acción"
#     },
#     {
#         "id": 2,
#         "title": "Avatar",
#         "overview": "Aventuras de ciencia ficción sobre alienígenas",
#         "year": "2009",
#         "rating": 7.8,
#         "category": "Acción"
#     }
# 

@app.get('/', tags=['home']) # home
def message():
    return HTMLResponse('<h1>Hola Mundo!</h1>')