# Instead of writing raw SQL queries to fetch or update records, ORMs allow 
# you to define classes and attributes that map directly to database tables and columns.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DB_URL = 'postgresql://postgres:7890@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DB_URL )  #manages connections to the database.

SessionLocal = sessionmaker(autoflush=False, bind=engine,autocommit = False )

class Base(DeclarativeBase):  #Creates the base class that all ORM models will inherit from.
    pass

def get_db():   #Defines a dependency function that provides a database session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Creates a session factory that generates database sessions using the engine.
autoflush=False → Changes are not automatically sent to the database before queries.
bind=engine → Associates every session with the created database engine.
autocommit=False → Transactions must be committed manually using db.commit()."""