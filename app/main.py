#runs the app
from fastapi import FastAPI
from app.routes import auth, product, cart, order
from app.db import database
from app.models import user  # This ensures the User model is registered

#This line creates the tables in the database if they don't exist
user.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
def root():
    return {"Message": "Ecommerce API is running"}
