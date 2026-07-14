from jose import JWTError,jwt
from datetime import datetime,timedelta
from. import schemas
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer

#OAuth2PasswordBearer automatically extracts the JWT from the Authorization: 
# Bearer <token> header and passes it to your function, while tokenUrl="login" tells FastAPI where clients obtain that token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#For token genration we need secret key, algorith and expiry time.

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Once hashed pwd and pwd sent by the client is verified, server generates the JWT which the client stores in its local storage.
def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
  
    return encoded_jwt

#encoded_jwt is not directly passed to verify_access_token(). It comes back from the client in the HTTP request.
#This function checks whether the JWT is valid and, if it is, extracts the user_id from it so FastAPI knows which user is making the request
def verify_access_token(token : str , credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  #Decodes the JWT using the secret key. If the token is invalid, tampered with, or expired, it raises JWTError.
        id : int = payload.get("user_id") #Extracts the user_id from the token payload.
        print(f"payload = {payload}")
        if id is None:  #If the token doesn't contain a user_id, treat it as invalid.
            raise credentials_exception
        token_data = schemas.Token_Data(id = id)  #Stores the extracted user ID in a Pydantic model for validation and easy access

    except JWTError:
    
        raise credentials_exception
    
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme)): #oauth2_scheme extracts the JWT from the request header and passes it to:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate credentials.',
                                         headers={"WWW-Authenticate" : "Bearer"})

    return verify_access_token(token, credentials_exception)
                                         