from tests.test_config.config import TestConfig
from config import Config

groups_template = [
    {"id": 1, "name": Config.APP_DEFAULT_ADMIN_GROUP},
    {"id": 2, "name": TestConfig.STANDARD_GROUP_NAME},
]

group_id_template = {
    "id": 2,
    "name": TestConfig.STANDARD_GROUP_NAME,
    "users": [
        {
            'id': 2,
            'username': TestConfig.STANDARD_USERNAME,
            'keys': [
                {
                    'id': 2,
                    'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY,
                    'comment': 'Test Key',
                }
            ]
        }
    ]
}
