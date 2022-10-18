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

