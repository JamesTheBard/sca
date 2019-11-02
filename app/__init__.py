from flask import Flask, jsonify
from config import Config
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes.auth import routes
from app.routes.users import routes
from app.routes.groups import routes
from app.routes.keys import routes
from app.models import users, groups, ssh_keys, user_groups_relationship

