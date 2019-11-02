from app import db
from app.models.user_groups_relationship import usergroups


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(100), unique=True, nullable=False)
    has_users = db.relationship(
        'User',
        secondary=usergroups,
        lazy='subquery',
        backref=db.backref('groups', lazy=True)
    )
