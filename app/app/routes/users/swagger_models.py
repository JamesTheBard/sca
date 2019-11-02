from app import api
from flask_restplus import fields


users_route_response = api.model('UsersRouteResponse', {
    'id': fields.Integer(description='The user ID'),
    'username': fields.String(description='The username of the user'),
})

user_create_request = api.model('UserCreate', {
    'username': fields.String(description='The username of the user', required=True),
    'password': fields.String(description='The password of the user'),
})

user_create_response = api.model('UserCreateResponse', {
    'id': fields.String(description="The ID of the user"),
    'username': fields.String(description="The username of the user"),
})

user_modify_request = api.model('UserModify', {
    'username': fields.String(description='The username of the user'),
    'password': fields.String(description='The password of the user'),
})

user_modify_response = api.model('UserCreateResponse', {
    'id': fields.String(description="The ID of the user"),
    'username': fields.String(description="The username of the user"),
})

group_info_response = api.model('KeyListResponse', {
    'id': fields.Integer(description="The ID of the group"),
    'name': fields.String(description="The name of the group")
})

key_info_response = api.model('KeyInfoResponse', {
    'id': fields.Integer(description="The key ID"),
    'pub_ssh_key': fields.String(description="Public SSH key (contents of .pub file)"),
    'comment': fields.String(description="Optional key description/comment")
})

user_info_response = api.model('UserInfoResponse', {
    'id': fields.Integer(description="The ID of the user"),
    'username': fields.String(description="The username of the user"),
    'pub_ssh_keys': fields.List(fields.Nested(key_info_response, description="The public SSH keys of the user")),
    'groups': fields.List(fields.Nested(group_info_response, description="Associated group information"))
})

key_create_request = api.model('KeyCreateRequest', {
    'pub_ssh_key': fields.String(description="Public SSH key (contents of .pub file)", required=True),
    'comment': fields.String(description="Optional key description/comment")
})

