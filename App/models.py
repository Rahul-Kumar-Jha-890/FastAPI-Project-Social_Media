#Every model represents a table in a db.
#Using ORM we create tables and queries through python file.
#database.py = How to connect to the database.
#models.py = What the database tables look like.

from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Integer,Column,String,Boolean,DateTime,ForeignKey
from datetime import datetime,timezone
from sqlalchemy.sql.expression import null
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key = True,nullable = False)
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,default = True, nullable=False)
    
    created_at = Column(
    DateTime(timezone=True),
    nullable=False,
    server_default=func.now()
)
    owner_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable = False)
    owner = relationship("Users")

class Users(Base):
     __tablename__ = "users"

     id = Column(Integer,primary_key = True,nullable = False)
     email = Column(String, nullable=False,unique=True)
     password = Column(String,nullable=False)
     created_at = Column(
    DateTime(timezone=True),
    nullable=False,
    server_default=func.now())

class Vote(Base):
     __tablename__ = "votes"

     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),primary_key=True)
     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"),primary_key=True)