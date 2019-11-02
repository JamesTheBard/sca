from tests.test_config.config import TestConfig
from config import Config

users_get_response = [
    {
        "id": 1,
        "username": Config.APP_DEFAULT_USERNAME,
    },
    {
        "id": 2,
        "username": TestConfig.STANDARD_USERNAME,
    },
]

user_id_get_adm_response = {
    'id': 1,
    'username': Config.APP_DEFAULT_USERNAME,
    'keys': [],
    'groups': [
        {'id': 1, 'name': Config.APP_DEFAULT_ADMIN_GROUP}
    ]
}

user_id_get_std_response = {
    'id': 2,
    'username': 'John Smith',
    'keys': [
        {'id': 1, 'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY, 'comment': None}
    ],
    'groups': []
}