from fastapi import Path, Query,Request,HTTPException, Depends, APIRouter
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from authentication_jwt.autenthication_w_jwt import validateToken
from fastapi.security import HTTPBearer
from database_sql_alchemy.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder

movieRouter = APIRouter()


class Movie (BaseModel):
    id:Optional[int]=None #se le indica que en un principio va a ser none
    title:str = Field(default="Título de la película", min_length=1 ,max_length=100)
    director:str = Field(default="Director de la película", min_length=1 ,max_length=100)
    overview:str = Field(default="Descripción de la película", min_length=1 ,max_length=1000)
    year:int = Field(default="2023")
    rating:float = Field(default="Rating de la película", ge=1, le=10)
    category:str = Field(default="Categoria de la película", min_length=1 ,max_length=50)

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data["email"] != "a@a.com":
            raise HTTPException(status_code=401, detail="Invalid credentials")


@movieRouter.get('/movies', tags=["Movies"], dependencies=[Depends(BearerJWT())])
def get_all_movies():
    connection = Session()
    data_movies = connection.query(ModelMovie).all()
    connection.close()
    return JSONResponse(content=jsonable_encoder(data_movies))

@movieRouter.get('/movies/{id}', tags=["Movies"])
def get_movie(id: int = Path(ge=1,le=100)):
    connection = Session()
    data_movie = connection.query(ModelMovie).filter_by(id=id).first()
    if not data_movie:
        connection.close()
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    connection.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(data_movie))

@movieRouter.get('/movies/', tags=["Movies"], status_code=200)
def get_movies_by_category(category: str = Query(min_length=3,max_length=100)):

    formmated_category =  category.capitalize()

    connection = Session()
    data_movie = connection.query(ModelMovie).filter_by(category=formmated_category).all()
    if not data_movie:
        connection.close()
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    connection.close()
    return JSONResponse(content = jsonable_encoder(data_movie))


@movieRouter.post('/movies/', tags=["Movies"], status_code=201)
def create_movie(movie: Movie):
    # movies.append(movie)
    connection = Session()
    new_movie = ModelMovie(**movie.model_dump()) # ** se le pasan todos los parametros
    connection.add(new_movie)
    connection.commit() #para guardar los datos
    connection.close()
    # return JSONResponse(content={"message": "Movie Created", "movie" : [m for m in movies]})
    return JSONResponse(content={"message": "Movie Created"})

@movieRouter.put('/movies/{id}', tags=["Movies"])
def update_movie(id: int,movie: Movie):
    connection = Session()
    data_movie = connection.query(ModelMovie).filter_by(id=id).first()

    if not data_movie:
        connection.close()
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    data_movie.title = movie.title
    data_movie.director = movie.director
    data_movie.overview = movie.overview
    data_movie.year = movie.year
    data_movie.rating = movie.rating
    data_movie.category = movie.category
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Movie Updated"})

@movieRouter.delete('/movies/{id}', tags=["Movies"],status_code=200 )
def delete_movie(id: int):

    connection = Session()

    movie_data = connection.query(ModelMovie).filter_by(id=id).first()
    if not movie_data:
        connection.close()
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    connection.delete(movie_data)
    # movie_data.delete()
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Movie Deleted"})