from jwt import encode, decode

def createtoken(data: dict) -> str:
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token

def validatetoken(token: str) -> dict:
    data: dict = decode(token, key="my_secret_key", algorithms=['HS256'])
    return data