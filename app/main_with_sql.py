# FAST API processes requests in order. It finds the first method that matches then the matching url: "/"
# Fundamentally an API is a bunch of path operations.

# from typing import Optional # no longer used
from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body # no longer used
from pydantic import BaseModel
# from random import randrange # no longer used
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    """ 
    This class helps to validate the schema for the posts we expect from the API user i.e frontend.
    From pydantic's docs different data types can be specified
    """
    title: str
    content: str
    published: bool = True # If user does not provide a value for published, it will default to true
    
    #rating: Optional[int] = None # If user does not provide a value for Optional it will default to None

while True:
    try:
        # remember to use env vars before posting on github
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='Abbason719psql', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)




# Stand-in data store
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# path operation 
@app.get("/") # decorator
async def root(): # In the case of this app, async keyword (used for asynchronous operations) not required
    return {"message": "Welcome to my API. It's the best!"}

@app.get("/posts") # e.g /posts, /users (Convention. Always plural.)
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):                          # in fxn argument the post data is validated and cast as a pydantic model.  
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
   
                       (post.title, post.content, post.published))      
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/latest") # Order matters. With how Fast API works this matches with /posts/{id} and if it were after it, searching for this path would yield /posts/{id} producing an error
def get_post(): 
    post = my_posts[len(my_posts) - 1]
    return{"detail": post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found" )
       
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()
    # if old post does not exist, throw up 404 error
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    
    return {"data": updated_post}






































