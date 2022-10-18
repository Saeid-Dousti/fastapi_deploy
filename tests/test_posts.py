import pytest
from typing import List
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    print(posts_list)
    # posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts_list) == len(test_posts)
    assert res.status_code ==  200

def test_unauthorized_user_get_all_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/post/99999")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published",[
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "no thanks", False),
    ("tallest skyscraper", "milad tower maybe?", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title":title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title":"arbitrary title", "content": "asdfaf"})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "asdfaf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']    


def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title":"arbitrary title", "content": "asdfaf"})

    assert res.status_code == 401
