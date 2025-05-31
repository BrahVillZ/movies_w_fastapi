from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database_sql_alchemy.database import engine,Base
from routers.movie import movieRouter
from routers.login import loginRouter
app = FastAPI(
    title="Aprendiendo FastApi",
    description="Aprendiendo FastApi",
    version="0.0.1"
)

app.include_router(movieRouter)
app.include_router(loginRouter)

Base.metadata.create_all(bind=engine) #creación de la base de datos

@app.get('/', tags=["inicio"])
def road_root():
    return HTMLResponse("<h2>¡Bienvenido Brah!</h2>")






