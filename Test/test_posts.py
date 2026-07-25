def test_get_post(authorized_client,test_posts):
    res = authorized_client.get("/posts")
    #print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_post(client,test_posts):
    res = client.get("/posts/")
    print(dict(client.headers))
    assert res.status_code == 401

def test_unauthorized_user_get_all_post_id(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(dict(client.headers))
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/8899")
    assert res.status_code == 404