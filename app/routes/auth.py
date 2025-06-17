#authentication api route / logic for user registration, user login and jwt authentication
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.schemas.user import UserRegister, UserLogin
from app.models.user import User
from app.db.database import get_db
from app.auth.jwt_handler import create_access_token, get_current_user

router = APIRouter(tags=["Auth"]) #creates group of endpoints under the auth tag
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
#check if user already exists
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed = pwd_context.hash(user.password) #hash the user password
    new_user = User(email=user.email, password=hashed, role=user.role) #object new_user to add to database
    db.add(new_user)
    db.commit() #save new user in the database
    db.refresh(new_user)
    return {"msg": "User created successfully"} #confirmation

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email, "role": db_user.role, "id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}

