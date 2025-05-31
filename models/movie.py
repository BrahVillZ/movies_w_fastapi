from database_sql_alchemy.database import Base
from sqlalchemy import Column,Integer,String,Float

class Movie (Base):
    __tablename__ : str = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    director = Column(String(100))
    overview = Column(String(1000))
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String(100))
