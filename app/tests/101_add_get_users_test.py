from config import Config
from tests.test_config.config import TestConfig
from tests.conftest import login
from tests.responses import users


def test_users_path(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    assert r_std.token
    assert r_std.response.status_code == 200
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)
    assert r_adm.token
    assert r_adm.response.status_code == 200

    response = client.get('/users', headers=r_std.headers)
    assert response.status_code == 200
    assert response.json == users.users_get_response

    response = client.get('/users', headers=r_adm.headers)
    print(response.json)
    assert response.status_code == 200
    assert response.json == users.users_get_response


def test_user_id_path(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    data = {'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY}
    response = client.put('/user/2/key', json=data, headers=r_std.headers)
    assert response.status_code == 200

    creds = [r_std, r_adm]
    for cred in creds:
        response = client.get('/user/1', headers=r_std.headers)
        assert response.status_code == 200
        assert response.json == users.user_id_get_adm_response
        response = client.get('/user/2', headers=r_std.headers)
        print(response.json)
        assert response.status_code == 200
        assert response.json == users.user_id_get_std_response

    response = client.delete('/user/2/key/1', headers=r_adm.headers)
    assert response.status_code == 200
