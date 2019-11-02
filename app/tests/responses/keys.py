from tests.test_config.config import TestConfig

user_key_get_response = [
    {
        'id': 2,
        'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY,
        'comment': 'Test Key'
    }
]

keys_get_response = [
    {'id': 1, 'pub_ssh_key': TestConfig.ADMIN_PUB_SSH_KEY, 'comment': 'Test Key'},
    {'id': 2, 'pub_ssh_key': TestConfig.STANDARD_PUB_SSH_KEY, 'comment': 'Test Key'},
]