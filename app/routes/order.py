from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.auth.jwt_handler import get_current_user
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderOut, OrderUpdateStatus
from app.utils.email_sender import send_order_email
from app.models.user import User # to get email

router = APIRouter(prefix="/orders", tags=["Orders"]) #object to create endpoints under orders tags

#place an order from cart
@router.post("/", response_model=OrderOut)
def place_order(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user["id"]).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    order_items = []

    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue  # skip deleted product
        subtotal = product.price * item.quantity
        total += subtotal
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        ))

    order = Order(
        user_id=current_user["id"],
        total=round(total, 2),
        items=order_items
    )
    db.add(order)
    db.query(CartItem).filter(CartItem.user_id == current_user["id"]).delete()  # clear cart
    db.commit()
    db.refresh(order)

    #get user's email
    user = db.query(User).filter(User.id == current_user["id"]).first()

    #order summary
    order_summary = f"Hi {user.email}, \n\nThanks for your order #{order.id}!n\nOrder Items:\n"
    for item in order_items:
        order_summary += f"- Product ID: {item.product_id}, Qty: {item.quantity}, Price: ${item.price}\n"
    order_summary += f"\nTotal: ${order.total}\n\nWe’ll notify you when it ships."

    send_order_email(user.email, order_summary)

    return order

#view user past orders
@router.get("/{user_id}", response_model=list[OrderOut])
def get_orders(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Order).filter(Order.user_id == user_id).all()

#admin only update order status e.g shipped
@router.patch("/{order_id}")
def update_order_status(order_id: int, status_data: OrderUpdateStatus, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_data.status
    db.commit()
    return {"msg": "Order status updated"}
