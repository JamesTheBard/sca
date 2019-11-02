from config import Config
from tests.test_config.config import TestConfig
from tests.conftest import login
from tests.responses import keys


def test_user_key_put(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    # Adding an SSH key to the admin account, admin should pass, standard should fail
    creds = {
        401: r_std,
        200: r_adm,
    }
    data = {
        'pub_ssh_key': TestConfig.ADMIN_PUB_SSH_KEY,
        'comment': 'Test Key',
    }
    for cred in creds.keys():
        response = client.put('/user/1/key', json=data, headers=creds[cred].headers)
        assert response.status_code == cred
        if response.status_code == 200:
            assert response.json['id'] == 1
            assert response.json['pub_ssh_key'] == TestConfig.ADMIN_PUB_SSH_KEY

    # Attempting to upload the same SSH key twice, should fail
    creds = {403: r_std, 403: r_adm}
    for cred in creds.keys():
        response = client.put('/user/2/key', json=data, headers=creds[cred].headers)
        print(response.json)
        assert response.status_code == cred

    # Adding a key to the standard account, both should pass
    data = {
        'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY,
        'comment': 'Test Key',
    }
    creds = {200: r_std, 200: r_adm}
    for cred in creds.keys():
        response = client.put('/user/2/key', json=data, headers=creds[cred].headers)
        print(response.json)
        assert response.status_code == cred
        assert response.json['id'] == 2
        assert response.json['pub_ssh_key'] == TestConfig.STANDARD_PUB_SSH_KEY


def test_keys_get_route(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = {200: r_adm}
    for cred in creds:
        response = client.get('/keys', headers=creds[cred].headers)
        print(response.json)
        assert response.status_code == cred
        if response.status_code == 200:
            assert response.json == keys.keys_get_response


def test_user_key_get_route(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = [r_std, r_adm]
    for cred in creds:
        response = client.get('/user/2/keys', headers=cred.headers)
        assert response.status_code == 200
        assert response.json == keys.user_key_get_response
