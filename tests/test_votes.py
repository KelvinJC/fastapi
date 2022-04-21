import pytest   
from app import models

# test_vote_on_post is the case of a user voting on their own post
# since as per current design, the app allows for it.
# If it becomes required to prevent such then the app itself must be updated 
# and a specific test to check against that be designed

def test_vote_on_post(authorised_client, test_posts):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == 201

'''
def test_vote_own_post(authorised_client, test_user, test_posts):
    # This test is to be applied only under the implementation where users cannot vote on their own posts and the above test becomes unrequired
    res = authorised_client.post("/vote/", json={"post_id": test_posts[0].id, "dir":1})
    assert res.status_code == 403
'''

def test_vote_on_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 201

'''
A fixture function defined inside a test file has a scope within the test file only. 
That fixture cannot be used in another test file. 
This fixture function is defined here since it is only for use in test_vote_twice_post
'''

@pytest.fixture      
def test_vote(test_posts, session, test_user):
    # vote on the 4th post by adding vote to the database directly 
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_twice_post(authorised_client, test_posts, test_vote):
    # Test users ability to vote twice (in the same direction) on the same post
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 409

def test_delete_vote(authorised_client, test_posts, test_vote):
    # Test users ability to delete vote 
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":0})
    assert res.status_code == 201

def test_delete_non_exist_vote(authorised_client, test_posts):
    # Test users ability to delete non existent vote 
    res = authorised_client.post("/vote/", json={"post_id": test_posts[3].id, "dir":0})
    assert res.status_code == 404


def test_vote_non_exist_post(authorised_client, test_vote):
    # Test users ability to vote a non existent post 
    res = authorised_client.post("/vote/", json={"post_id": 80000, "dir":1})
    assert res.status_code == 404

def test_vote_unauthorised(client, test_posts):
    # Test unauthorised users ability to vote on a post
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir":1})
    assert res.status_code == 401