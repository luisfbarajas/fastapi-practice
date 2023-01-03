#Python native
from typing import Optional, List

#pydantic
from pydantic import BaseModel, Field


#FastAPI
from fastapi import FastAPI, Body,Path,status, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#my function
from jwt_manager import createtoken,validatetoken

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validatetoken(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")


class User(BaseModel):
    email:str
    password:str

class Movies(BaseModel):
    id:Optional[int] = Field(...,description='id',title='ID',example='1234')
    title: str = Field(..., title='Title of movie',description='Title of movie', example='My movie test')
    overview: str = Field(...,title='Overview',description='Resume about the movie',example='this is my overview')
    year:int = Field(..., title='Year',description='Year of de movie', example= 2022)
    raiting: float = Field(...,title='Raiting', description='raiting for the movie', example=8.5)
    category: str = Field(..., title="category", description='Category of the movie', example='Action')

app = FastAPI()


app.title = "Doumentacion de Fast API"

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

@app.post("/login", tags=['Login'])
def Login(user:User):
    token = createtoken(user.dict())
    return JSONResponse(status_code=status.HTTP_200_OK,content=token)

@app.get("/", tags=['home'])
def home():
    return HTMLResponse("HelloWrold")

@app.get("/movies", tags=['movies'],response_model=List[Movies],status_code=status.HTTP_200_OK,dependencies=[Depends(JWTBearer())])
def getMovies() -> List[Movies]:
    return JSONResponse(status_code=200 ,content=movies)

@app.get("/movies/{id}", tags=['movies'],status_code=status.HTTP_200_OK)    
def getMovie(id: int):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=[])

@app.get("/movies/",tags=['movies'],description="Get a movie by a query parameter",status_code=status.HTTP_200_OK)
def getMoviesByCategory(category:str, year:int ):
    # for item in movies:
    #     if item["category"] == category and int(item["year"]) == year:
    #         return item
    data =[item for item in movies if item["category"] == category and int(item["year"]) == year]
    return  JSONResponse(content=data)

@app.post('/movies', tags=['movies'],status_code=status.HTTP_201_CREATED)
def createMovie(movie: Movies):
    movies.append(movie)
    return JSONResponse(content={"message": "Succes register"})

@app.put("/movies/{id}", tags=['movies'])
def updateMovie(  movie: Movies, id: int = Path(
        ..., 
        gt=0,
        example=123
        )  ):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item["category"] = movie.category
            item["year"] = movie.year
            item["raiting"] = movie.rating
            item["overview"] = movie.overview
            return JSONResponse(content={"message": "Succes update"})


@app.delete("/movies/{id}", tags=['movies'])
def deleteMovie(    id: int = Path(
        ..., 
        gt=0,
        example=123
        )):
    for item in movies:
        movies.remove(item)
        return JSONResponse(content={"message": "Succes delete"})
