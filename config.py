import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    JWT_SECRET_KEY = 'Rr9xK%lliD&8*@Gf0Z*x8Lz&Hy07pLsA#BEi9F6KmS3WF5qn0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{}'.format(os.path.join(basedir, 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_DEFAULT_USERNAME = os.environ.get('APP_DEFAULT_USERNAME') or 'admin'
    APP_DEFAULT_PASSWORD = os.environ.get('APP_DEFAULT_PASSWORD') or 'password'
    APP_DEFAULT_ADMIN_GROUP = os.environ.get('APP_DEFAULT_ADMIN_GROUP') or 'sca_admin'
    RESTPLUS_VALIDATE = True