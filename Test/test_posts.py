from App import schemas
import pytest

#Every test insert 2 posts in our test db.
"""def test_get_post(authorized_client,test_posts):
    res = authorized_client.get("/posts")
    #print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_post(client,test_posts):
    res = client.get("/posts/")
    #print(dict(client.headers))
    assert res.status_code == 401

def test_unauthorized_user_get_all_post_id(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
   # print(dict(client.headers))
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/8899")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[2].id}")
    post = schemas.PostOut(**res.json())  #pydantic validation
   # print(post)
    assert post.Post.id == test_posts[2].id
#models.Post → the SQLAlchemy class representing the posts table.
#session.query(models.Post) → queries the posts table and returns Post objects.

@pytest.mark.parametrize("title, content, published", [
    ("new post 1", "content of post 1", True),
    ("new post 2", "content of post 2", True),
    ("new post 3", "content of post 3", False),
])
def test_create_post(authorized_client,title, content, published, test_user):
    res = authorized_client.post("/posts/", json={"title": title, "content" : content, "published" : published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_user_create_post(client,test_user):
     res = client.get(f"/posts/")
     assert res.status_code == 401

def test_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/ {test_posts[0].id}")
    assert res.status_code == 204

def test_unauthorized_post_delete(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_not_exist(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/ 800000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403"""

def test_update_post(authorized_client,test_posts):
    data = {   #This is the new data we want the API to save
        "title" : "Updated title",
        "content" : "Updated content",
        "id" : test_posts[0].id 
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json= data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client,test_posts):
      data = {   #This is the new data we want the API to save
            "title" : "Updated title",
            "content" : "Updated content",
            "id" : test_posts[2].id 
        }
    
      res = authorized_client.put(f"/posts/{test_posts[2].id}", json= data)
      assert res.status_code == 403

def test_unauthorized_post_update(client,test_user,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client,test_posts):
    data = {   #This is the new data we want the API to save
            "title" : "Updated title",
            "content" : "Updated content",
            "id" : test_posts[0].id 
        }
    res = authorized_client.put(f"/posts/ 800000", json=data)
    assert res.status_code == 404