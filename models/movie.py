from config.database import base
from sqlalchemy import Column, Integer, String, Float

class Movie(base):
    __tablename__ = "movies"

    id= Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    raiting = Column(Float)
    category = Column(String)