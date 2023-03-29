import pytest
from src import init_app
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
    Attempt to register a user with an existing username
    """
    auth.register()
    response = auth.register()
    assert response.status_code == 400


def test_login(client, auth):
    """
    Log in
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
