from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token

# Create a dummy database for testing purposes
SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# create engine to talk to the database
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    '''
    Provides access to test database.
    Drop all tables from previous test. 
    This prevents the hitches of duplicating data during repeated testing
    
    Returns:
    db: obj. Database object
    '''
    Base.metadata.drop_all(bind=engine)
    # create new tables before test
    Base.metadata.create_all(bind=engine)
    # create database session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function") # scope= function is the default. left here as note
def client(session): # A pytest fixture can pass in another pytest fixture function as an argument
    '''
    Calls session fixture before executing 

    Returns:
    TestClient: obj. 
        Object with app as its argument. Similar to the the Response object in the Requests library
    '''
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # swaps get_db fxn with override_get_db throughout app 
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)                        
                            
    # ---- the db manipulation can also be done with alembic ----
    # from alembic import command
    # command.upgrade("head")
    # yield TestClient(app)
    # command.downgrade("base")

@pytest.fixture()
def test_user2(client):
    """
    Calls client fixture before executing
    """
    user_data = {"email": "kelvin002@gmail.com",
                    "password": "password1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user(client):
    """
    Calls client fixture before executing
    """
    user_data = {"email": "kelvin@gmail.com",
                    "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    """
    Calls test_user fixture before executing.
    Uses the create token fxn from oauth2 module
    """
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorised_client(client, token):
    """
    Calls client and token fixtures before executing
    Returns: obj
    client - an authenticated client
    """
    client.headers = {
        # unpack the current headers
        **client.headers,
        # add the the token to the header
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    """
    Calls session and test_user fixtures before executing
    """
    posts_data = [{
        "title": "first title",
        "content":"first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content":"2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content":"3rd content",
        "owner_id": test_user['id']
    },{
        "title": "4th title",
        "content":"3rd content",
        "owner_id": test_user2['id']
    }]
    
    # to insert all the above user posts into a database session
    # create a function to unpack the content of a dictionary
    def create_post_model(post):
        return models.Post(**post)
    # then map the created function to the array of 
    # dictionaries which represents the posts
    post_map = map(create_post_model, posts_data)
    # convert map object to a list
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts