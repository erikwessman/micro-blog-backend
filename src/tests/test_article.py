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


def post_article(client, token, title='test title'):
    """
    Helper method for posting articles
    """
    return client.post("/api/article/user", content_type="application/json",
                       json={
                           'title': title,
                           'description': 'test description',
                           'categories': ['test'],
                           'content': 'test content'
                       },
                       headers={
                           'Authorization': token
                       })


def register_and_get_token(auth):
    """
    Helper method for registering a user and returning a token for authentication
    """
    auth_response = auth.register()
    response_dict = json.loads(auth_response.data)
    return (response_dict['token'])


def test_article_post(client, auth):
    """
    Post an article and fetch it
    """
    token = register_and_get_token(auth)
    article_res = post_article(client, token)
    article_id = article_res.data.decode('utf-8')

    response = client.get(f'/api/article?id={article_id}',
                          content_type="application/json")
    article = json.loads(response.data)

    assert response.status_code == 200
    assert article['title'] == 'test title'


def test_article_patch(client, auth):
    """
    Update an article and fetch it, test the change
    """
    token = register_and_get_token(auth)
    article_res = post_article(client, token)
    article_id = article_res.data.decode('utf-8')

    client.patch(f'/api/article?id={article_id}', content_type="application/json",
                 json={
                     'content': 'changed'
                 })

    response = client.get(f'/api/article?id={article_id}',
                          content_type="application/json")
    article = json.loads(response.data)

    assert response.status_code == 200
    assert article['content'] == 'changed'


def test_article_delete(client, auth):
    """
    Delete an article
    """
    token = register_and_get_token(auth)
    article_res = post_article(client, token)
    article_id = article_res.data.decode('utf-8')

    client.delete(f'/api/article?id={article_id}',
                  content_type="application/json")

    response = client.get(f'/api/comment?id={article_id}',
                          content_type="application/json")

    assert response.status_code == 404


def test_article_validate(client, auth):
    """
    Test the validation of the article JSON schema
    """
    token = register_and_get_token(auth)
    response = post_article(client, token, None)

    assert response.status_code == 400
