import random

import pytest
import requests


@pytest.mark.parametrize('value', [0, 101, 55, 100])
def test_posts_id(value):
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{value}')
    data = response.json()
    if 0 < value <= 100:
        assert 200 == response.status_code
        assert "OK" == response.reason
        assert data['id'] == value
    else:
        assert 404 == response.status_code
        assert "Not Found" == response.reason


def test_create_post():
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    body = {"title": "foo", "body": "bar", "userId": 1, "id": 40}
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=body, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 101
    for key, value in body.items():
        if key != "id":
            assert data[key] == value


def test_checking_post_comments():
    comment_id = random.randint(1, 500)
    print(f"Checking comment {comment_id}")
    response = requests.get(f'https://jsonplaceholder.typicode.com/comments/{comment_id}')
    assert response.status_code == 200
    comment_data = response.json()
    post_id = comment_data['postId']
    email_in_comment = comment_data['email']

    response_post = requests.get(f'https://jsonplaceholder.typicode.com/comments?postId={post_id}')
    assert response.status_code == 200
    post_comments = response_post.json()
    post_comments_id = []
    for comment in post_comments:
        post_comments_id.append(comment['id'])
        if comment['email'] == email_in_comment:
            for key in comment_data:
                assert comment_data[key] == comment[key]
    assert comment_id in post_comments_id


# @pytest.mark.skip(reason="test markers")
@pytest.mark.parametrize('url', ['https://jsonplaceholder.typicode.com/comments/1',
                                 'https://jsonplaceholder.typicode.com/albums/1'])
def test_delete(url):
    response = requests.delete(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.parametrize('field, value', [('email', 'newtest@mail.to'), ('name', 'New Name')])
def test_patching(field, value):
    user_id = random.randint(1, 10)
    print(f"Checking comment {user_id}")

    response = requests.get(f'https://jsonplaceholder.typicode.com/users/{user_id}')
    assert response.status_code == 200
    original_data = response.json()

    headers = {'Content-type': 'application/json; charset=UTF-8'}
    body = {field: value}
    response = requests.patch(f'https://jsonplaceholder.typicode.com/users/{user_id}', json=body, headers=headers)
    modified_data = response.json()
    assert response.status_code == 200

    for i in modified_data:
        if field == i:
            assert original_data[i] != modified_data[i]
            assert value == modified_data[i]
        else:
            assert original_data[i] == modified_data[i]
