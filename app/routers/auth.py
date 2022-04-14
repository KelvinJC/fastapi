from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication']) 


# login endpoint
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):     # OAuth2PasswordRequestForm is a dictionary with keys username and password. Username key can have an email or whatever you choose as its value

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credential")

    # create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # 'data' goes into payload. It can include user role, scope of endpoints which user can access etc. For now I'm sticking with id
    
    return {"access_token": access_token, "token_type": "bearer"}
