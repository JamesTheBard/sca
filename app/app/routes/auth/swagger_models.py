from app import api
from flask_restplus import fields


login_model = api.model('LoginModel', {
    'username': fields.String(description='The username to log in as', required=True),
    'password': fields.String(description='The password associated with the user', required=True)
})

login_model_response = api.model('LoginModelResponse', {
    'access_token': fields.String(description='The JWT access token')
})
