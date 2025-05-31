import jwt
from jwt import encode

def createToken (data: dict):
    token : str = encode(payload=data, key="mysecret", algorithm="HS256")
    #token : str =  jwt.encode(payload=data,key="mysecret",algorithm="HS256")
    return token

def validateToken (token: str)->dict:
    data = jwt.decode(token, key="mysecret", algorithms=["HS256"])
    return data
