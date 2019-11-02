from config import Config
from tests.test_config.config import TestConfig
from tests.conftest import login
from tests.responses import groups


def test_group_put(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = {
        401: r_std,
        200: r_adm,
    }
    data = {'name': TestConfig.STANDARD_GROUP_NAME}
    for cred in creds:
        response = client.put(
            "/group",
            json={"name": TestConfig.STANDARD_GROUP_NAME},
            headers=creds[cred].headers,
        )
        assert response.status_code == cred
        if response.status_code == 200:
            assert response.json['name'] == 'Test Group'


def test_groups_get(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = [r_std, r_adm]
    for cred in creds:
        response = client.get('/groups', headers=cred.headers)
        assert response.status_code == 200
        print(response.json)
        assert response.json == groups.groups_template


def test_group_user_put(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = {401: r_std, 200: r_adm}
    for cred in creds:
        response = client.put('/group/2/user/2', headers=creds[cred].headers)
        assert response.status_code == cred


def test_group_id_get(client):
    r_std = login(client, TestConfig.STANDARD_USERNAME, TestConfig.STANDARD_PASSWORD)
    r_adm = login(client, Config.APP_DEFAULT_USERNAME, Config.APP_DEFAULT_PASSWORD)

    creds = [r_std, r_adm]
    for cred in creds:
        response = client.get('/group/2', headers=cred.headers)
        print(response.json)
        assert response.json == groups.group_id_template



