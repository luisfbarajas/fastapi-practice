#FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
#my function
from config.database import engine,base
from routers.movie import movieRouter
from routers.users import userRouter
from middlewares.errorHandler import ErrorHandler

app = FastAPI()

app.title = "Doumentacion de Fast API"
app.add_middleware(ErrorHandler)
app.include_router(movieRouter)
app.include_router(userRouter)

base.metadata.create_all(bind=engine)

@app.get("/", tags=['home'])
def home():
    return HTMLResponse("HelloWrold")
