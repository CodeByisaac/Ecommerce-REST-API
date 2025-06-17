# define order and order item models for the ecommerce system
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

#represents a order made by a user
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")
    total = Column(Float) #total cost of the order

    #one to mant relationship: and order can have multiple items
    items = relationship("OrderItem", back_populates="order")

#single item in an order
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)  # snapshot price

    #reference back to parent order
    order = relationship("Order", back_populates="items")
