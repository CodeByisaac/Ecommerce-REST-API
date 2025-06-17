
#how fast api talks to database with sqlalchemy
from sqlalchemy import create_engine #actual connection to database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://ecommerce_db_cvkv_user:TqYLa1G5iKbLnHHcqoKDMl7cbnLQdgLj@dpg-d18mb26mcj7s73a5qc70-a/ecommerce_db_cvkv"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base() #creates a base class for defining models
#dependency that gives session and closes up
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

