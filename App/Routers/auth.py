from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from ..import database,schemas,models,utils,oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

#Receive login credentials → Find user → Verify password → Generate JWT → Return token.

@router.post("/login")
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = f'Invalid Credentials.')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                           detail =  f'Invalid Credentials.')
    
   #Create a token , return token.

    access_token = oauth2.create_access_token(data={"user_id" : user.id})

    return{"access_token" : access_token , "token_type" : "bearer"}

#user is simply the authenticated user's row from the database, represented as a SQLAlchemy object
#of the user who is trying to log in.