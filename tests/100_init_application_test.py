from flask_migrate import upgrade
from tests.config import TestConfig
from tests.conftest import login
import os


def test_init_database(client):
    upgrade(directory='migrations', revision='head')
    assert os.path.exists('app.db')


def test_init_application(client):
    response = client.post("/init")
    assert response.status_code == 200


def test_init_username(client):
    r = login(client)
    assert r.token
    assert r.response.status_code == 200


def test_create_standard_user(client):
    r = login(client)
    assert r.response.status_code == 200
    codes = [200, 400]
    for code in codes:
        response = client.put(
            "/user",
            json={
                "username": TestConfig.STANDARD_USERNAME,
                "password": TestConfig.STANDARD_PASSWORD,
            },
            headers={"Authorization": "Bearer {}".format(r.token)}
        )
        assert response.status_code == code
        if response.status_code == 200:
            assert response.json['username'] == "John Smith"

    codes = [200, 400]
    assert r.response.status_code == 200
    for code in codes:
        response = client.put(
            "/group",
            json={"name": TestConfig.STANDARD_GROUP_NAME},
            headers={"Authorization": "Bearer {}".format(r.token)}
        )
        assert response.status_code == code
        if response.status_code == 200:
            assert response.json['name'] == 'Test Group'


def test_standard_login(client):
    r = login(client, "John Smith", "test_password")
    assert r.token
    assert r.response.status_code == 200
