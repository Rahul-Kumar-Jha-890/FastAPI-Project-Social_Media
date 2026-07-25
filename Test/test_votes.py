import pytest
from App import models

@pytest.fixture()  #Adds a vote
def add_vote(test_posts,session,test_user):
    new_vote = models.Vote(post_id =test_posts[0].id, user_id = test_user["id"])
    session.add(new_vote)
    session.commit()

#test_posts[0].id → gets the ID of the first post (e.g., 1).
#test_user["id"] → gets the ID of the test user (e.g., 1).

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote", json={"post_id" : test_posts[0].id, "dir" : 1})
    assert res.status_code == 201

def test_duplicate_vote(authorized_client,test_posts,add_vote):
    res = authorized_client.post("/vote/", json={"post_id" : test_posts[0].id,"dir" : 1})
    assert res.status_code == 409

def test_delete_vote(authorized_client,test_posts,add_vote):
    res = authorized_client.post("/vote/", json={"post_id" : test_posts[0].id,"dir" : 0})
    assert res.status_code == 201

def test_delete_vote_non_existent(authorized_client,test_posts):
     res = authorized_client.post("/vote/", json={"post_id" : test_posts[0].id,"dir" : 0})
     assert res.status_code == 404

def test_vote_post_non_existent(authorized_client,test_posts):
    res = authorized_client.post("/vote/", json={"post_id" : 8000, "dir" : 0})
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir" : 1})
    assert res.status_code == 401