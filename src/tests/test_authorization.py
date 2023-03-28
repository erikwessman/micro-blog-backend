import pytest
from src import init_app


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


def test_register(client):
    """
    Register a user
    Assert that the request is successful with status code 200
    """
    response = client.post("/api/authorization/register", content_type="application/json",
                           json={
                               'username': 'user',
                               'email': 'user@gmail.com',
                               'password': 'password'
                           })
    assert response.status_code == 200


def test_register_validate(client):
    """
    Attempt to register a user without submitting an email
    Request will fail because email is a required field
    Assert that the request fails with status code 400
    """
    response = client.post("/api/authorization/register", content_type="application/json",
                           json={
                               'username': 'user',
                               'password': 'password'
                           })
    assert response.status_code == 400


def test_register_existing_username(client):
    """
    Register a user and attempt to create a second user with the same username as the first
    Request will fail because usernames must be unique
    Assert that the request fails with status code 400
    """
    client.post("/api/authorization/register", content_type="application/json",
                json={
                    'username': 'user',
                    'email': 'user@gmail.com',
                    'password': 'password'
                })

    response = client.post("/api/authorization/register", content_type="application/json",
                           json={
                               'username': 'user',
                               'email': 'another_user@gmail.com',
                               'password': 'password'
                           })
    assert response.status_code == 400


def test_register_existing_email(client):
    """
    Register a user and attempt to create a second user with the same email as the first
    Request will fail because email addresses must be unique
    Assert that the request fails with status code 400
    """
    client.post("/api/authorization/register", content_type="application/json",
                json={
                    'username': 'user',
                    'email': 'user@gmail.com',
                    'password': 'password'
                })

    response = client.post("/api/authorization/register", content_type="application/json",
                           json={
                               'username': 'another_user',
                               'email': 'user@gmail.com',
                               'password': 'password'
                           })
    assert response.status_code == 400


def test_login(client):
    """
    Register a user and attempt to log in
    Assert that the request is successful with status code 200
    """
    client.post("/api/authorization/register", content_type="application/json",
                json={
                    'username': 'user',
                    'email': 'user@gmail.com',
                    'password': 'password'
                })

    response = client.post("/api/authorization/login", content_type="application/json",
                           json={
                               'username': 'user',
                               'password': 'password'
                           })
    assert response.status_code == 200


def test_login_validate(client):
    """
    Attempt to log in without submitting a password in the request
    Request will fail because logging in requires both a username and password
    Assert that the request fails with status code 400
    """
    response = client.post("/api/authorization/login", content_type="application/json",
                           json={
                               'username': 'user',
                           })
    assert response.status_code == 400


def test_login_wrong_password(client):
    """
    Register a user then attempt to log in with the existing username using an incorrect password
    Request will fail because the password will not match
    Asser that the request fails with status code 400
    """
    client.post("/api/authorization/register", content_type="application/json",
                json={
                    'username': 'user',
                    'email': 'user@gmail.com',
                    'password': 'password'
                })

    response = client.post("/api/authorization/login", content_type="application/json",
                           json={
                               'username': 'user',
                               'password': 'password1'
                           })
    assert response.status_code == 400
