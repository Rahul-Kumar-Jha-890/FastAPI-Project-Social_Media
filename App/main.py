from fastapi import FastAPI
from. import models
from .database import engine
from .Routers import posts, users,auth,votes
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine) #Creates all database tables defined in your ORM models if they don't already exist.


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

