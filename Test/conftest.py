from fastapi.testclient import TestClient
from App.main import app
from App.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from App.oauth2 import create_access_token
from App.database import get_db,Base
import pytest
from App import models

SQLALCHEMY_DB_URL = SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DB_URL )  #manages connections to the database.

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine,autocommit = False )

@pytest.fixture(scope="module")  #The database is shared across all tests in the file.
def session():
       Base.metadata.drop_all(bind=engine)  #Drop all tables
       Base.metadata.create_all(bind=engine) #Create all tables
       db = TestingSessionLocal()   #Creates a SQLAlchemy session(connection) to that database.
       try:
            yield db    #yield db pauses the session fixture and gives the database session to the client fixture.
       finally:       #After test finishes, execution comes back to the fixture.
            db.close()

@pytest.fixture(scope="module")   #Before creating the client fixture, pytest must first create the session fixture
def client(session ):
    def override_get_db():   #Defines a dependency function that provides a database session

        try:
            yield session  
        finally:     
            session.close()

    app.dependency_overrides[get_db] = override_get_db  #Redirects all test ops from real db to test db.
    yield TestClient(app)   #TestClient  ───────►  FastAPI App
    #yield TestClient(app) pauses the client fixture and gives the client object to the test.
    
@pytest.fixture(scope="module")
def test_user(client):
    user_data = {"email" : "rj@gmail.com", "password" : "7890"}  #create a user and insert in test db.
    res = client.post("/users/" , json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user  #returns email and pwd of new user for test_login_user

@pytest.fixture(scope="module")
def token(test_user):
    return create_access_token({"user_id" : test_user["id"]})  #returns JWT . id is the unique identifier stored in the token as user_id

@pytest.fixture
def authorized_client(client,token):
     client.headers = {
          **client.headers,  #Copy all existing headers and add one more.
          "Authorization" : f"Bearer {token}"  #Gets added to client header. Passed from client to server with every HTTP request.
     }
     yield client

     client.headers.pop("Authorization", None)  #prevents auth token leakage between tests
     return client

@pytest.fixture  #Sample data to populate our db for testing test_get_post
def test_posts(session,test_user): #session -> Gives a SQLAlchemy database session connected to the test database.

     session.add_all([models.Post(title = "first title",content = "first content", owner_id = test_user["id"]),
                      models.Post(title="Second title" , content = "first content", owner_id = test_user["id"])])

     session.commit()
     query = session.query(models.Post).all()
     return query