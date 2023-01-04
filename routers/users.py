#fastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import JSONResponse
from utils.jwt_manager import createtoken
from schemas.user import User

userRouter = APIRouter()

@userRouter.post("/login", tags=['Login'])
def Login(user:User):
    token = createtoken(user.dict())
    return JSONResponse(status_code=status.HTTP_200_OK,content=token)
