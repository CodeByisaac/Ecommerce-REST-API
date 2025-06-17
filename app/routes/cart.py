from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session #mangages db transaction query add delete items
from app.db.database import get_db
from app.auth.jwt_handler import get_current_user
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart import AddToCart, CartItemOut, CartResponse, CartItemProduct

router = APIRouter(prefix="/cart", tags=["cart"]) #object to create endpoints under cart tag
@router.post("/", response_model=CartItemOut)
def add_to_cart(
    item: AddToCart,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    #to avoid dublicates, increase quantity of product if already in cart
    existing = db.query(CartItem).filter(
        CartItem.user_id == current_user["id"],
        CartItem.product_id == item.product_id
    ).first()

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        cart_item = existing

    else:
        new_item = CartItem(
            user_id=current_user["id"],
            product_id = item.product_id,
            quantity=item.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        cart_item =  new_item
    return {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "item_total": round(product.price * cart_item.quantity, 2)
    }

@router.get("/", response_model=CartResponse)
def view_cart(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    items = db.query(CartItem).filter(CartItem.user_id == current_user["id"]).all()

    response_items = []
    total = 0

    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue  # in case product was deleted

        item_total = product.price * item.quantity
        total += item_total

        response_items.append(
            CartItemOut(
                id=item.id,
                quantity=item.quantity,
                product=product,
                item_total=round(item_total, 2)
            )
        )

    return CartResponse(items=response_items, total=round(total, 2)) #return both list of items and total cost

@router.delete("/item/{item_id}")
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not item or item.user_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Item not found or unauthorized")
    db.delete(item)
    db.commit()
    return {"msg": "Item removed from cart"}
