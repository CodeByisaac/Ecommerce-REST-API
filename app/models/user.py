#Creating our users table in Postgresql
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Base


class User(Base):   #Defines a new table called users
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True)
    password = Column(String)
    role = Column(String, default = "customer")
