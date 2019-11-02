import os


def test_destroy_database():
    os.remove('app.db')
    assert not os.path.exists('app.db')
