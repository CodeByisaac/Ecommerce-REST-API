#to validate users data
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "customer" #default role

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#return only necessary info to client
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True #tell pydantic to read data if from ORM model
