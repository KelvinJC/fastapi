# conftest.py files are package specific. 
# All files within a package have access to it 
# without the need for importing. 
# If a new package called api is created within tests package
# and it contains a file test_pack.py, 
# test_pack.py would have access to this conftest.py
# also if a new conftest.py were within the api package
# test_pack.py would have access to the new conftest.py but tests in the outer package e.g test_users.py would not.

import pytest
from jose import jwt
from app import schemas 
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == "Hello World! Welcome to my API. It's the best!"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json())
    print(res.json())

    #assert res.json().get("email") == "hello123@gmail.com"
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# test_create_user can also access the database by passing in session as an argument
# e.g
# def test_create_user(client, session):
#     post_query = session.query(models.Post)
#     post = post_query.first()

def test_login_user(client, test_user):
    # recall that login request is sent as a form and field in Oauth form is 'username'
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 201 # changed from 200 


@pytest.mark.parametrize("email, password, status_code", [
        ('wrongemail@gmail.com', 'password123', 403),
        ('kelvin@gmail.com', 'wrongpassword', 403),
        ('wrongemail@gmail.com', 'wrongpassword', 403),
        (None, 'password123', 422),
        ('kelvin@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'  # Since 'Invalid Credentials' response won't apply when the server response is a 422 error

 