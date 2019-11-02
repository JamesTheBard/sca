from app import db
from app.models.user_groups_relationship import usergroups
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    keys = db.relationship('SSHKey', backref='user', lazy=True)
    in_groups = db.relationship(
        'Group',
        secondary=usergroups,
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
