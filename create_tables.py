from app.db.database import engine
from app.models.user import Base as UserBase
from app.models.product import Base as ProductBase
from app.models.cart import Base as CartBase
from app.models.order import Base as OrderBase

# Create tables based on model metadata
UserBase.metadata.create_all(bind=engine)
ProductBase.metadata.create_all(bind=engine)
CartBase.metadata.create_all(bind=engine)
OrderBase.metadata.create_all(bind=engine)

print("Tables created successfully.")
