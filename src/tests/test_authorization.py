import pytest
from src import init_app
from src.db import DBManager


@pytest.fixture
def client():
    app = init_app()
    app.config.update({
        "TESTING": True,
        "DB_NAME": "micro-blog-test"
    })

    yield app.test_client()

    DBManager.drop_all()


def test_app(client):
    response = client.get("/", content_type="application/json")
    assert response.status_code == 200


def test_add(client):
    response = client.post("/api/user", content_type="application/json",
                           json={
                               'username': 'okk',
                               'email': 'okk@gmail.com',
                               'password': 'pass'
                           })
    assert response.status_code == 200
