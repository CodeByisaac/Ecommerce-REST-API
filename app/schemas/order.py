#data validation pydantic to check if value passed is the correct data type
from pydantic import BaseModel
from typing import List

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    total: float
    status: str
    items: List[OrderItemOut]

    class Config:
        from_attributes=True

class OrderUpdateStatus(BaseModel):
    status: str
