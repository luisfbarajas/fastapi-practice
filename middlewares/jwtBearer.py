from fastapi.security import HTTPBearer
from fastapi import Request,HTTPException
from utils.jwt_manager import createtoken,validatetoken

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validatetoken(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
