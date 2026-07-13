from fastapi import FastAPI,Response,HTTPException,status,Depends
from pydantic import BaseModel
from. import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from .Routers import posts, users,auth

models.Base.metadata.create_all(bind=engine) #Creates all database tables defined in your ORM models if they don't already exist.


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


