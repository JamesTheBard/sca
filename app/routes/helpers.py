from app import api, db, app
from flask import abort, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from sqlalchemy import inspect
from app.models.users import User
from app.models.groups import Group

token_parser = api.parser()
token_parser.add_argument(
    'Authorization',
    location='headers',
    type=str,
    help='Bearer Access Token',
    required=True
)


def init():
    u = User.query.all()
    if not u:
        admin_user = User(
            username=app.config['APP_DEFAULT_USERNAME'],
        )
        admin_user.set_password(app.config['APP_DEFAULT_PASSWORD'])
        admin_group = Group(
            name=app.config['APP_DEFAULT_ADMIN_GROUP']
        )
        admin_user.in_groups.append(admin_group)
        db.session.add(admin_user)
        db.session.add(admin_group)
        db.session.commit()


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            abort(401, 'Not Authorized')
        return f(*args, **kwargs)
    return wrap


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
