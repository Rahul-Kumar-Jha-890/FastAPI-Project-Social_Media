from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing import Annotated

class PostBase(BaseModel):
    title : str
    content:str
    published : bool = True 

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):  #Pydantic model for data validation.
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post : Post
    Votes:int
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

class Token(BaseModel):
    acess_token : str
    token_type : str

class Token_Data(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : Annotated[int, Field(ge=0, le=1)]