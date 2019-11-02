from app import api, db
from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from app.models.groups import Group
from app.models.users import User
from app.routes.groups import swagger_models
from app.routes.helpers import token_parser, is_admin, object_as_dict


@api.route('/groups')
class GroupsInfoRoute(Resource):
    @api.doc(parser=token_parser)
    @api.marshal_with(swagger_models.group_route_response)
    @api.response(401, 'Not Authorized')
    @jwt_required
    def get(self):
        """
        Gets all groups in the database
        """
        groups = Group.query.all()
        return groups, 200


@api.route('/group')
class GroupCreateRoute(Resource):
    @api.doc(parser=token_parser, body=swagger_models.group_route_request)
    @api.response(200, 'Success', swagger_models.group_route_response)
    @api.response(400, 'Bad Request')
    @api.response(401, 'Not Authorized')
    @jwt_required
    @is_admin
    def put(self):
        """
        Create a group in the database
        """
        g = Group.query.filter_by(name=request.json['name']).first()
        if g:
            return {'msg': 'Group already exists'}, 400
        g = Group()
        [setattr(g, i[0], i[1]) for i in request.json.items()]
        db.session.add(g)
        db.session.commit()
        return object_as_dict(g), 200


@api.route('/group/<int:group_id>')
class GroupModifyRoute(Resource):
    @api.doc(parser=token_parser)
    @api.response(200, 'Success', swagger_models.group_info_response)
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    def get(self, group_id):
        """
        Get all users and keys from a group
        """
        g = Group.query.filter_by(id=group_id).first()
        if not g:
            return {'msg': 'Group not found'}, 404
        group_info = object_as_dict(g)
        users_info = list()
        for u in g.has_users:
            temp = {
                "id": u.id,
                "username": u.username,
                "keys": [{'id': k.id, 'pub_ssh_key': k.pub_ssh_key, 'comment': k.comment} for k in u.keys]
            }
            users_info.append(temp)
        group_info['users'] = users_info
        return group_info, 200

    @api.doc(parser=token_parser, body=swagger_models.group_route_request)
    @api.response(200, 'Success', swagger_models.group_route_response)
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def put(self, group_id):
        """
        Modify the name of a group
        """
        g = Group.query.filter_by(id=group_id).first()
        if not g:
            return {'msg': 'Group not found'}, 404
        [setattr(g, i[0], i[1]) for i in request.json.items()]
        db.session.add(g)
        db.session.commit()
        return object_as_dict(g), 200

    @api.doc(parser=token_parser, body=swagger_models.group_route_request)
    @api.response(200, 'Success', swagger_models.group_route_request)
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def delete(self, group_id):
        """
        Delete a group in the database
        """
        g = Group.query.filter_by(id=group_id).delete()
        if not g:
            return {'msg': 'Group not found'}, 404
        db.session.commit()


@api.route('/group/<int:group_id>/user/<int:user_id>')
class GroupAssociateUsersRoute(Resource):
    @api.doc(parser=token_parser)
    @api.response(200, 'Success')
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def put(self, group_id, user_id):
        """
        Attach user to a given group
        """
        g = Group.query.filter_by(id=group_id).first()
        if not g:
            return {'msg': 'Group not found'}
        u = User.query.filter_by(id=user_id).first()
        if not u:
            return {'msg': 'User not found'}
        g.has_users.append(u)
        db.session.add(g)
        db.session.add(u)
        db.session.commit()

    @api.doc(parser=token_parser)
    @api.response(200, 'Success')
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def delete(self, group_id, user_id):
        """
        Remove a user from a given group
        """
        g = Group.query.filter_by(id=group_id).first()
        if not g:
            return {'msg': 'Group not found'}
        u = User.query.filter_by(id=user_id).first()
        if not u:
            return {'msg': 'User not found'}
        g.has_users.remove(u)
        db.session.add(g)
        db.session.add(u)
        db.session.commit()
