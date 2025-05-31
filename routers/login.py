from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from authentication_jwt.autenthication_w_jwt import createToken

loginRouter = APIRouter(tags=["Login"])

class User(BaseModel):
    email: str
    password: str

@loginRouter.post('/login', tags=["Login"])
def login(user: User):
    if user.email == "a@a.com" and user.password == "123":
        token : str = createToken(user.model_dump())
        print(token)
        return JSONResponse(content=token)
    return user
