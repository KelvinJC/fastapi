from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from requests import Session
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # the string login here is from the login endpoint i.e. /login path operation

 
# all settings.x values are read into the program from environment variables
# create a secret key
SECRET_KEY = settings.secret_key        
# select algorithm to be deployed in hashing token
ALGORITHM = settings.algorithm    
# specify time to expiration of token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() # create copy of the data to be put in the token

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # token expiration time to end session 
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    # alternative implementation to fetching user from db in every path operation
    token = verify_access_token(token, credentials_exception) 
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # with former implementation return verify_access_token(token, credentials_exception)
    return user

