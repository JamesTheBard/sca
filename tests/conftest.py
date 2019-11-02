import os
import pytest
from sca import create_app
from config import Config
from collections import namedtuple
from flask_migrate import upgrade


LoginInfo = namedtuple('LoginInfo', ['token', 'response', 'headers'])


def login(client, user: str = Config.APP_DEFAULT_USERNAME, password: str = Config.APP_DEFAULT_PASSWORD):
    response = client.post(
        "/login", json={"username": user, "password": password}
    )
    print(user, response.json)
    return LoginInfo(
        token=response.json['access_token'],
        response=response,
        headers={"Authorization": "Bearer {}".format(response.json['access_token'])},
    )


@pytest.fixture()
def app():
    app = create_app()
    return app
