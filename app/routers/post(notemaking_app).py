from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse]) # e.g /posts, /users (Convention. Always plural.)
def get_posts(db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    #  With current_user as dependency, this fxn will run only if the user has been authenticated i.e. has a token
    #  This is optional. Not critical in all apps. For example users may see other users posts/tweets without logging in on Twitter through a web search 
    
    # Fetch all posts made by the user
    # Use case could be a notemaking app where notes made by user are intended to be private. 
    # I intend to adapt this to SIMS' note maker for teachers
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):                          # in fxn argument the post data is validated and cast as a pydantic model.  
    
    #  With current_user as dependency, this fxn will run only if the user has been authenticated i.e. has a token
    
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # known as **kwargs... **post.dict() is a more efficient way to represent line above. It unpacks the dictionary 
    db.add(new_post)
    db.commit() # surprisingly, at first posts were committed without commit and add fxns.... puzzling!
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    #  With current_user as dependency, this fxn will run only if the user has been authenticated i.e. has a token
    #  This is optional. Not critical in all apps. For example users may see other users posts/tweets without logging in on Twitter through a web search 

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found" )
    # Users can retrieve only the posts i.e. notes they create
    # Use case could be a notemaking app where notes made by user are intended to be private. 
    # I intend to adapt this to SIMS' note maker for teachers
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorised to perform requested action")  

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
   # Ensure posts only get deleted by the owner
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorised to perform requested action")
    

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router .put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: object = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # if post to be updated does not exist, throw up 404 error
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    # Ensure posts only get updated by the owner
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorised to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()