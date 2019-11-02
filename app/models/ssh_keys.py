from app import db


class SSHKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_ssh_key = db.Column(db.String(300))
    comment = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
