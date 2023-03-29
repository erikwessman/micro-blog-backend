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


def create_user(client, username='test'):
    """
    Helper method for creating users
    """
    return client.post("/api/user", content_type="application/json",
                       json={
                           'username': username,
                           'email': 'test@test.gmail.com',
                           'password': 'test'
                       })


def test_user_create(client, auth):
    """
    Create a user and fetch it
    """
    user_res = create_user(client)
    user_id = user_res.data.decode('utf-8')

    response = client.get(f'/api/user?id={user_id}',
                          content_type="application/json")
    user = json.loads(response.data)

    assert response.status_code == 200
    assert user['username'] == 'test'


def test_user_patch(client, auth):
    """
    Create a user and update it, test the change
    """
    user_res = create_user(client)
    user_id = user_res.data.decode('utf-8')

    client.patch(f'/api/user?id={user_id}', content_type="application/json",
                 json={
                     'username': 'user'
                 })

    response = client.get(f'/api/user?id={user_id}',
                          content_type="application/json")
    user = json.loads(response.data)

    assert response.status_code == 200
    assert user['username'] == 'user'


def test_user_delete(client, auth):
    """
    Delete a user
    """
    user_res = create_user(client)
    user_id = user_res.data.decode('utf-8')

    client.delete(f'/api/user?id={user_id}', content_type="application/json")

    response = client.get(f'/api/user?id={user_id}',
                          content_type="application/json")

    assert response.status_code == 404


def test_user_validate(client, auth):
    """
    Test the validation of the user JSON schema
    """
    response = create_user(client, None)

    assert response.status_code == 400
