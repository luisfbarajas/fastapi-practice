from pydantic import BaseModel,Field
from typing import Optional

class Movies(BaseModel):
    id:Optional[int] = None
    title: str = Field(..., title='Title of movie',description='Title of movie', example='My movie test')
    overview: str = Field(...,title='Overview',description='Resume about the movie',example='this is my overview')
    year:int = Field(..., title='Year',description='Year of de movie', example= 2022)
    raiting: float = Field(...,title='Raiting', description='raiting for the movie', example=8.5)
    category: str = Field(..., title="category", description='Category of the movie', example='Action')
