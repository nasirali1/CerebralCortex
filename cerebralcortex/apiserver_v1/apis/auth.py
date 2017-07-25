from cerebralcortex.apiserver_v1 import CC
from cerebralcortex.apiserver_v1.core.decorators import auth_required
from cerebralcortex.apiserver_v1.core.data_models import auth_data_model
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_raw_jwt, decode_token
from flask_restplus import Namespace, Resource
from datetime import datetime, timedelta

auth_route = CC.configuration['routes']['auth']
auth_api = Namespace(auth_route, description='Authentication service')



@auth_api.route('/')
class Auth(Resource):
    @auth_api.doc('')
    @auth_api.expect(auth_data_model(auth_api), validate=True)
    @auth_api.response(400, 'User name and password cannot be empty.')
    @auth_api.response(401, 'Wrong username or password.')
    #@auth_api.doc(params={"header":"Content-Type: application/json"})
    #@auth_api.marshal_list_with(auth_data_model(auth_api))
    def post(self):
        '''Post authentication credentials'''
        username = request.json.get('email_id', None).strip()
        password = request.json.get('password', None).strip()
        print(username+"=="+password)
        if not username or not password:
            return {"msg": "User name and password cannot be empty."}, 401

        if not CC.login_user(username,password):
            return {"msg": "Wrong username or password"}, 401

        token_issue_time = datetime.now()
        expires = timedelta(seconds=int(CC.configuration['apiserver']['token_expire_time']))
        token_expiry = token_issue_time + expires

        token = create_access_token(identity=username, expires_delta=expires)

        # Identity can be any data that is json serializable
        access_token = {'access_token': token}
        CC.update_auth_token(username, token, token_issue_time, token_expiry)
        return access_token, 200

    @auth_required
    @auth_api.header("Authorization", 'Bearer JWT', required=True)
    def get(self):
        '''Sample route to test authentication'''
        return "working!", 200