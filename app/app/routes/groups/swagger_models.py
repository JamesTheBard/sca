from app import api, db
from flask_restplus import fields


group_route_response = api.model('GroupRouteResponse', {
    'id': fields.Integer(description='The group ID'),
    'name': fields.String(description='The name of the group'),
})

group_route_request = api.model('GroupRouteRequest', {
    'name': fields.String(description='The name of the group', required=True),
})

group_modify_response = api.model('GroupModifyResponse', {
    'name': fields.String(description='The name of the group'),
})

group_keys_info_response = api.model('GroupKeyInfoResponse', {
    'id': fields.Integer(description='The ID of the key associated with the user'),
    'pub_ssh_key': fields.String(description='The public SSH key associated with the user')
})

group_user_info_response = api.model('GroupUserInfoResponse', {
    'id': fields.Integer(description='The user ID of the user in the group'),
    'username': fields.String(description='The username of the group user'),
    'keys': fields.List(fields.Nested(group_keys_info_response, description='Public SSH key information'))
})

group_info_response = api.model('GroupInfoResponse', {
    'id': fields.Integer(description='The group ID'),
    'name': fields.String(description='The name of the group'),
    'users': fields.List(fields.Nested(group_user_info_response, description='User information'))
})