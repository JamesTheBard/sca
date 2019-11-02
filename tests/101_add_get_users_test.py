from config import Config
from tests.config import TestConfig
from tests.conftest import login


USERS_OUTPUT = [
    {
        "id": 1,
        "username": Config.APP_DEFAULT_USERNAME,
    },
    {
        "id": 2,
        "username": TestConfig.STANDARD_USERNAME,
    },
]


def test_users_path(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    assert r_std.token
    assert r_std.response.status_code == 200
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)
    assert r_adm.token
    assert r_adm.response.status_code == 200

    response = client.get('/users', headers=r_std.headers)
    assert response.status_code == 200
    assert response.json == USERS_OUTPUT

    response = client.get('/users', headers=r_adm.headers)
    print(response.json)
    assert response.status_code == 200
    assert response.json == USERS_OUTPUT


def test_user_id_path(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = [r_std, r_adm]
    for cred in creds:
        response = client.get('/user/1', headers=r_std.headers)
        print(response.json.keys())
        assert response.status_code == 200
        assert len(response.json.keys()) == 4
        response = client.get('/user/2', headers=r_std.headers)
        assert response.status_code == 200
        assert len(response.json.keys()) == 4
