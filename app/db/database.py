
#how fast api talks to database with sqlalchemy
from sqlalchemy import create_engine #actual connection to database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base() #creates a base class for defining models
#dependency that gives session and closes up
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

