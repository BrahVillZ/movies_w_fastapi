import os #Crea funct que interactuan con nuestro so
from sqlalchemy import create_engine #crea conexiones con la db
from sqlalchemy.orm import sessionmaker #usa expresiones declarativas
from sqlalchemy.ext.declarative import declarative_base

#Crear la db en esa ruta
sqliteName = "movies.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))
databaseUrl = f"sqlite:///{os.path.join(base_dir, sqliteName)}"

#Crear ahora el engine

engine = create_engine(databaseUrl,echo=True)

#crear la sesión

Session = sessionmaker(bind=engine)

#Usar la clase declarativa, se va a usar como una base de datos que representara las tablas

Base = declarative_base()