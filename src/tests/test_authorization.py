import pytest
from src import init_app


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username='test', email='test@test.com', password='test'):
        return self._client.post(
            '/api/authorization/register',
            content_type='application/json',
            json={
                'username': username,
                'email': email,
                'password': password
            })

    def login(self, username='test', password='test'):
        return self._client.post(
            '/api/authorization/login',
            content_type='application/json',
            json={
                'username': username,
                'password': password
            })


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


def test_register(client, auth):
    """
    Register a user
    """
    response = auth.register()
    assert response.status_code == 200


def test_register_validate(client, auth):
    """
    Attempt to register a user without submitting an email
    """
    response = auth.register(email=None)
    assert response.status_code == 400


def test_register_existing_username(client, auth):
    """
    Register a user with an existing username
    """
    auth.register()
    response = auth.register()
    assert response.status_code == 400


def test_login(client, auth):
    """
    Register a user and attempt to log in
    """
    auth.register()
    response = auth.login()
    assert response.status_code == 200


def test_login_validate(client, auth):
    """
    Attempt to log in without submitting a password in the request
    """
    response = auth.login(password=None)
    assert response.status_code == 400


def test_login_wrong_password(client, auth):
    """
    Attempt to log in with a wrong password
    """
    auth.register()
    response = auth.register(password='123')
    assert response.status_code == 400
