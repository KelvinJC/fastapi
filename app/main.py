# FAST API processes requests in order. It finds the first method that matches then the matching url: "/"
# Fundamentally an API is a bunch of path operations.

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings

# models.Base.metadata.create_all(bind=engine) # No longer needed now that Alembic now handles migrations

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# specify which requests the API can accept
# specify the headers API can accept

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# Path operations
@app.get("/") # decorator
def root(): # In the case of this router, async keyword (used for asynchronous operations) not required
    return {"message": "Welcome to my API. It's the best!"}

