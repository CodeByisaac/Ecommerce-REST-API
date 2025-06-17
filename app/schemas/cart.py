from pydantic import BaseModel

class CartItemProduct(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class AddToCart(BaseModel):
    product_id:int
    quantity:int

class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity:int
    item_total: float

    class Config:
        from_attributes=True

class CartResponse(BaseModel):
    items: list[CartItemOut]
    total: float
