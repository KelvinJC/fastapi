import pytest
from app import schemas
from tests.conftest import authorised_client

def test_get_all_posts(authorised_client, test_posts):
    """ 
    Test if an authenticated user is able to obtain all posts
    """
    res = authorised_client.get("/posts/")
    
    def validate(post):
        return schemas.PostVoted(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map) # can be used to further test each post response
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorised_user_get_all_posts(client, test_posts):
    """
    Test if an unauthenticated user is unable to get all posts
    """
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorised_user_get_one_posts(client, test_posts):
    """
    Test if an unauthenticated user is unable to get one post
    """
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorised_client, test_posts):
    """
    Test if an authenticated user is able to get a post which does not exist
    Post id is hard-coded for testing purposes. 
    """
    res = authorised_client.get(f"/posts/888888")
    assert res.status_code == 404

def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostVoted(**res.json())
    
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("well not so new title", "not so new content",  True),
     ("fave pizzas", "great pepperoni", False),
    ("tallest skyscrapers", "lofty buildings",  True) 
]) 
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorised_client, test_user, test_posts):
    res = authorised_client.post("/posts/", json={"title": "arbitrary title", "content": "content"})

    created_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorised_user_create_post(client, test_posts):
    """
    Test if an unauthenticated user is able to create posts
    """
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "content"})
    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    """
    Test if an unauthenticated user is able to delete posts
    """
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorised_user_delete_post_success(authorised_client, test_user, test_posts):
    """
    Test if an authenticated user is able to delete posts
    """
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_non_exist_post(authorised_client, test_posts, test_user):
    """
    Test if a user is able to delete a non existent post
    """
    res = authorised_client.delete(f"/posts/888888888")
    assert res.status_code == 404

def test_delete_other_user_post(authorised_client, test_posts, test_user):
    """
    Test if a user is able to delete another user's posts
    """
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorised_client, test_user, test_posts):
    """
    Test if a user is able to update posts
    """
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorised_client, test_user, test_user2, test_posts):
    """
    Test if a user is able to update another user's posts
    """
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_non_exist_post(authorised_client, test_posts, test_user):
    """
    Test if a user is able to delete a non existent post
    """
    data = {
        "title": "updated post",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/888888888", json=data)
    assert res.status_code == 404

def test_unauthorised_user_update_post(client, test_user, test_posts):
    """
    Test if an unauthenticated user is able to update another user's posts
    """
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

