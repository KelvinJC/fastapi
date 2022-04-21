from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication']) 


# login endpoint
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Server responds to a valid login attempt by sending client a JWT token     
    # Schema of login attempt is OAuth2PasswordRequestForm - a dictionary with keys as username and password.
    # 'Username' key can have a user's email or alternative required login info as its value
    # In this case username_credentials.username is an email

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # user login validation
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") # no user in database with that email
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials") # wrong password

    # create token with user id data as the payload. 
    # Payload can also include user role, scope of endpoints which user can access etc. 
    # only id used in this case
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) 
    return {"access_token": access_token, "token_type": "bearer"}
