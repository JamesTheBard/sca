from app import api, app
from flask import request, jsonify
from flask_restplus import Resource
from flask_jwt_extended import (
    create_access_token
)

from app.models.users import User
from app.models.groups import Group
from app.routes.auth.swagger_models import login_model, login_model_response
from app.routes.helpers import init


@api.route('/login')
class LoginRoute(Resource):
    @api.response(200, 'Success', login_model_response)
    @api.response(400, 'Validation Error')
    @api.response(401, 'Unauthorized')
    @api.expect(login_model)
    def post(self):
        """
        Logs into the API for the JWT authorization token
        """
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return {"msg": "Missing username"}, 400
        if not password:
            return {"msg": "Missing password"}, 400

        u = User.query.filter_by(username=username).first()
        if not u:
            return {"msg": "Bad username or password"}, 401
        if not u.check_password(password):
            return {"msg": "Bad username or password"}, 401

        g = Group.query.with_parent(u).filter_by(id=1).first()
        if g:
            access_token = create_access_token(identity={"username": username, "role": "admin"})
        else:
            access_token = create_access_token(identity={"username": username, "role": "standard"})
        return {"access_token": access_token}, 200


@api.route('/init')
class InitRoute(Resource):
    @api.response(200, 'Success')
    def post(self):
        """
        Initializes the application and creates initial user
        """
        init()
