from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr

from app.models import User

class PostBase(BaseModel):
    """ 
    This class validates the schema of the posts going from the user (i.e client/frontend) to the API .
    From pydantic's docs different data types can be specified
    """
    title: str
    content: str
    published: bool = True # If user does not provide a value for published, it will default to true
   
class PostCreate(PostBase):
    ''' This class inherits from PostBase and can have modifed attributes to serve the use case'''
    pass

# class PostUpdate(PostBase):

class UserOut(BaseModel): # placed here to give interpreter knowledge of the UserOut class that will be called in the PostResponse owner attribute
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        ''' Tells pydantic to convert the data it receives in a sqlalchemy model into data in a pydantic model'''
        orm_mode = True

class PostResponse(PostBase):
    """ 
    This class validates the schema of the response going from the API to the user (i.e client/frontend).
    It enables the streamlining of which fields the user receives, restricting or allowing any field chosen.
    In this case (to reduce the lines of code) it inherits attributes already specified by the parent class PostBase and adds new attributes
    """
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut         # infuses a Pydantic model of the owner into Post response. Yields a nested json string

    class Config:
        ''' Tells pydantic to convert the data it receives in a sqlalchemy model into data in a pydantic model'''
        orm_mode = True

class PostVoted(BaseModel):
    """ 
    This class validates the schema of voted posts going from the API to the user.
    """
    Post: PostResponse
    votes: int

    


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # This ensures that the integer recieved in the body of the token is either 0 or 1
