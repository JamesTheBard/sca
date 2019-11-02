from app import api, db
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from app.models.ssh_keys import SSHKey
from app.routes.users import swagger_models
from app.routes.helpers import token_parser, is_admin


@api.route('/keys')
class KeysRoute(Resource):
    @api.doc(parser=token_parser)
    @api.marshal_with(swagger_models.key_info_response, code=200)
    @api.response(401, 'Not Authorized')
    @jwt_required
    @is_admin
    def get(self):
        """
        Get all public SSH keys in the database.
        """
        keys = SSHKey.query.all()
        return keys, 200


@api.route('/key/<int:key_id>')
class DeleteKeyRoute(Resource):
    @api.doc(parser=token_parser)
    @api.response(200, 'Success', swagger_models.key_info_response)
    @api.response(401, 'Not Authorized')
    @api.response(404, 'Not Found')
    @jwt_required
    @is_admin
    def delete(self, key_id):
        """
        Delete a key in the database
        """
        k = SSHKey.query.filter_by(id=key_id).delete()
        if not k:
            return {'msg': 'Key does not exist'}
        db.session.commit()
