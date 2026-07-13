from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content:str
    published : bool = True 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):  #Pydantic model for data validation.
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True

# orm_mode=True integrates Pydantic models with ORMs by enabling     
# bidirectional data conversion between database ORM objects and Pydantic models

class UserLogin(BaseModel):
    email : EmailStr
    password : str