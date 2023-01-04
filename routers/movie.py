from fastapi import APIRouter
from middlewares.jwtBearer import JWTBearer
from models.movie import Movie as movieModel
from fastapi.encoders import jsonable_encoder
from fastapi import  Path,status, Depends
from typing import List
from fastapi.responses import  JSONResponse
from schemas.movie import Movies
from config.database import sesion
from services.movie import MovieServices

movieRouter = APIRouter()



movies = [{
    "id":1,
    "title": "Avatar",
    "overview": "It's an action movie in other world!",
    "year": "2009",
    "rating": 7.8,
    "category":"action"
},{
    "id":2,
    "title": "Avatar, the way of wather",
    "overview": "It's an action movie in other world!",
    "year": "2022",
    "rating": 8.8,
    "category":"action"
}]

@movieRouter.get("/movies", tags=['movies'],response_model=List[Movies],status_code=status.HTTP_200_OK,dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movies]:
    db = sesion()
    result = MovieServices(db).getMovies()
    return JSONResponse(status_code=status.HTTP_200_OK ,content=jsonable_encoder(result))

@movieRouter.get("/movies/{id}", tags=['movies'],status_code=status.HTTP_200_OK)    
def getMovie(id: int):
    db =  sesion()
    result =  MovieServices(db).getMovie(id=id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={'Message': 'Movie not found'})

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@movieRouter.get("/movies/",tags=['movies'],description="Get a movie by a query parameter",status_code=status.HTTP_200_OK)
def getMoviesByCategory(category:str):
    db = sesion()
    result = MovieServices(db=db).GetMovieByCategory(category=category)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'Messagge': 'Movie not found'})
    return  JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@movieRouter.post('/movies', tags=['movies'],status_code=status.HTTP_201_CREATED, response_model=dict)
def createMovie(movie: Movies) -> dict:
    db = sesion()
    MovieServices(db).CreateMovie(movie=movie)
    return JSONResponse(content={"message": "Succes register"})

@movieRouter.put("/movies/{id}", tags=['movies'], response_model=dict, status_code=status.HTTP_202_ACCEPTED)
def updateMovie(  movie: Movies, id: int = Path(
        ..., 
        gt=0,
        example=123
        )  ):
    db =  sesion()
    result =MovieServices(db=db).getMovie(id=id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not movie founded"})
    MovieServices(db=db).UpdateMovie(id=id,data=movie)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': 'Movie updated!'})


@movieRouter.delete("/movies/{id}", tags=['movies'],response_model=dict,status_code=status.HTTP_200_OK)
def deleteMovie(    id: int = Path(
        ..., 
        gt=0,
        example=123
        )):
    db =  sesion()
    result = MovieServices(db=db).getMovie(id=id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Not movie founded"})
    MovieServices(db=db).DeleteMovie(id=id)
    return JSONResponse(content={"message": "Succes delete"},status_code=status.HTTP_200_OK)
