import pytest
from src import init_app
import json
from .auth_actions import AuthActions


@pytest.fixture
def client():
    app = init_app()
    app.config.update({
        "TESTING": True,
        "DB_NAME": "micro-blog-test"
    })

    yield app.test_client()

    with app.app_context():
        from src.db import DBManager
        DBManager.drop_all()


@pytest.fixture
def auth(client):
    return AuthActions(client)


def post_comment(client, token, content='Test content'):
    return client.post("/api/comment/user", content_type="application/json",
                       json={
                           'content': content,
                           'article_id': '6413804cc4e64e5d1cd8e179'},
                       headers={
                           'Authorization': token
                       })


def register_and_get_token(auth):
    auth_response = auth.register()
    response_dict = json.loads(auth_response.data)
    return (response_dict['token'])


def test_comment(client, auth):
    """
    Post a comment and then fetch it
    """
    token = register_and_get_token(auth)
    comment_res = post_comment(client, token)
    comment_id = comment_res.data.decode('utf-8')

    response = client.get(f'/api/comment?id={comment_id}',
                          content_type="application/json")
    comment = json.loads(response.data)

    assert response.status_code == 200
    assert comment['author'] == 'test'


def test_get_comments_by_article(client, auth):
    """
    Post 2 comments under the same article and test that the length of that article's comments is 2
    """
    token = register_and_get_token(auth)
    post_comment(client, token)
    post_comment(client, token)

    response = client.get("/api/comment", content_type="application/json",
                          json={
                              'article_id': '6413804cc4e64e5d1cd8e179'
                          })

    comments = json.loads(response.data)
    assert response.status_code == 200
    assert len(comments) == 2


def test_patch_comment(client, auth):
    token = register_and_get_token(auth)
    comment_res = post_comment(client, token)
    comment_id = comment_res.data.decode('utf-8')

    client.patch(f'/api/comment?id={comment_id}', content_type="application/json",
                 json={
                     'content': 'test'
                 })

    response = client.get(f'/api/comment?id={comment_id}',
                          content_type="application/json")
    comment = json.loads(response.data)

    assert response.status_code == 200
    assert comment['content'] == 'test'


def test_delete_comment(client, auth):
    token = register_and_get_token(auth)
    comment_res = post_comment(client, token)
    comment_id = comment_res.data.decode('utf-8')

    client.delete(f'/api/comment?id={comment_id}',
                  content_type="application/json")

    response = client.get(f'/api/comment?id={comment_id}',
                          content_type="application/json")

    assert response.status_code == 404


def test_comment_validate(client, auth):
    token = register_and_get_token(auth)
    response = post_comment(client, token, None)

    assert response.status_code == 400
