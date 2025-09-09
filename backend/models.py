from sqlalchemy import Column, Integer, String
from .database import Base
class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String(64), unique=True, index=True, nullable=False)
    password_hash=Column(String(255), nullable=False)
class Movie(Base):
    __tablename__='movies'
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String(255), nullable=False)
    year=Column(Integer, nullable=False)
