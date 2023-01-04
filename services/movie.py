from models.movie import Movie as movieModel
from schemas.movie import Movies

class MovieServices:
    def __init__(self, db) -> None:
        self.db = db

    def getMovies(self):
        result = self.db.query(movieModel).all()
        return result

    def getMovie(self,id):
        result = self.db.query(movieModel).filter(movieModel.id == id).first()
        return result

    def GetMovieByCategory(self,category:str)->movieModel:
        result = self.db.query(movieModel).filter(movieModel.category == category).all()
        return result

    def CreateMovie(self, movie:Movies):
        newMovie = movieModel(**movie.dict())
        self.db.add(newMovie)
        self.db.commit()
        return

    def UpdateMovie(self,id:int,data:Movies):
        movie:Movies = self.db.query(movieModel).filter(movieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.raiting = data.raiting
        movie.category = data.category
        self.db.commit()
        return

    def DeleteMovie(self,id:int):
        self.db.query(movieModel).filter(movieModel.id == id).delete()
        self.db.commit()
        return