from app import api, db
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity


from app.models.users import User, users_restricted_fields
from app.models.ssh_keys import SSHKey
from app.routes.users import swagger_models
from app.routes.helpers import token_parser, is_admin, object_as_dict


@api.route('/users')
class UsersRoute(Resource):
    @api.marshal_with(swagger_models.users_route_response)
    @api.doc(parser=token_parser)
    @api.response(401, 'Not Authorized')
    @jwt_required
    def get(self):
        """
        Gets all users in the database
        """
        users = User.query.all()
        return users, 200


@api.route('/user')
class UserRouteNew(Resource):
    @api.doc(parser=token_parser, body=swagger_models.user_create_request)
    @api.response(200, 'Success', swagger_models.user_create_response)
    @api.response(400, 'Bad Request')
    @jwt_required
    @is_admin
    def put(self):
        """
        Creates a new user
        """
        u = User.query.filter_by(username=request.json['username']).first()
        if u:
            return {'msg': 'User already exists'}, 400
        u = User(username=request.json['username'])
        if 'password' in request.json.keys():
            u.set_password(request.json['password'])
        db.session.add(u)
        db.session.commit()
        return {"id": u.id, "username": u.username}, 200


@api.route('/user/<int:user_id>')
class UserRouteGetChange(Resource):
    @api.doc(parser=token_parser)
    @api.response(200, 'Success', swagger_models.user_info_response)
    @api.response(404, 'Not Found')
    @jwt_required
    def get(self, user_id):
        """
        Gets all associated information for a user
        """
        verify_jwt_in_request()
        identity = get_jwt_identity()
        u = User.query.filter_by(id=user_id).first()
        if not u:
            return {'msg': 'User not found'}, 404
        user = {"id": u.id, "username": u.username}
        keys = [{"id": k.id, "pub_ssh_key": k.pub_ssh_key, "comment": k.comment} for k in u.keys]
        user['keys'] = keys
        groups = list()
        for group in u.in_groups:
            template = {
                "id": group.id,
                "name": group.name
            }
            groups.append(template)
        user['groups'] = groups
        return user, 200

    @api.doc(parser=token_parser, body=swagger_models.user_modify_request)
    @api.response(200, 'Success', swagger_models.user_modify_response)
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def put(self, user_id):
        """
        Changes information for a user
        """
        u = User.query.filter_by(id=user_id).first()
        if not u:
            return {'msg': 'User not found'}, 404
        try:
            u.set_password(request.json['password'])
        except KeyError:
            pass
        [setattr(u, i[0], i[1]) for i in request.json.items() if i not in users_restricted_fields]
        db.session.add(u)
        db.session.commit()
        return {"id": u.id, "username": u.username}, 200

    @api.doc(parser=token_parser)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def delete(self, user_id):
        """
        Deletes a user from the database
        """
        if user_id == 1:
            return
        u = User.query.filter_by(id=user_id).delete()
        if not u:
            return {'msg': 'User not found'}, 404
        db.session.commit()
        return


@api.route('/user/<int:user_id>/keys')
class UserGetKeysRoute(Resource):
    @api.doc(parser=token_parser)
    @api.marshal_with(swagger_models.key_info_response)
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    def get(self, user_id):
        """
        Lists all associated public SSH keys for a user
        """
        u = User.query.filter_by(id=user_id).first()
        if not u:
            return {'msg': 'User not found'}, 404
        return [object_as_dict(i) for i in u.keys], 200


@api.route('/user/<int:user_id>/key')
class UserAddKeyRoute(Resource):
    @api.doc(parser=token_parser, body=swagger_models.key_create_request)
    @api.response(200, 'Success', swagger_models.key_info_response)
    @api.response(401, 'Not Authorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Not Found')
    @jwt_required
    def put(self, user_id):
        """
        Adds a key to a given user
        """
        verify_jwt_in_request()
        identity = get_jwt_identity()
        u = User.query.filter_by(id=user_id).first()
        if identity['role'] == 'standard' and u.username != identity['username']:
            return {'msg': 'Not authorized'}, 401
        if not u:
            return {'msg': 'User not found'}, 404
        if 'PRIVATE' in request.json['pub_ssh_key']:
            return {'msg': 'NO PRIVATE KEYS'}, 403
        k = SSHKey.query.filter_by(pub_ssh_key=request.json['pub_ssh_key']).first()
        if k:
            return {'msg': 'Key already exists'}, 403
        k = SSHKey()
        [setattr(k, i[0], i[1]) for i in request.json.items()]
        u.keys.append(k)
        db.session.add(u)
        db.session.add(k)
        db.session.commit()
        return {"id": k.id, "pub_ssh_key": k.pub_ssh_key, "comment": k.comment}, 200


@api.route('/user/<int:user_id>/key/<int:key_id>')
class UserKeyOperations(Resource):
    @api.doc(parser=token_parser)
    @api.response(200, 'Success')
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    def delete(self, user_id, key_id):
        """
        Delete public SSH key associated with a given user
        """
        verify_jwt_in_request()
        identity = get_jwt_identity()
        u = User.query.filter_by(id=user_id).first()
        if identity['role'] == 'standard' and u.username != identity['username']:
            return {'msg': 'Not authorized'}, 401
        if key_id not in [i.id for i in u.keys]:
            return {'msg': 'Key not found'}, 404
        k = SSHKey.query.filter_by(id=key_id).delete()
        db.session.commit()
