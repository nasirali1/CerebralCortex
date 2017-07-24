from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt_identity, decode_token, get_raw_jwt
from flask import request, jsonify

from datetime import datetime
import pytz

from cerebralcortex.apiserver_v1 import CC


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.replace("Bearer ", "")

        if not token:
            return {"msg" : "Token is missing!"}, 401

        #TODO: catch exception when token is expired
        try:
            decoded_token = decode_token(token)
        except Exception as e:
            return {"msg": str(e)}, 401



        auth_token_expiry_time = decoded_token['exp']

        #localizing time with time-zone
        auth_token_expiry_time = datetime.fromtimestamp(auth_token_expiry_time, tz=pytz.timezone(CC.time_zone))

        token_owner = decoded_token['identity']

        if not CC.is_auth_token_valid(token_owner, token, auth_token_expiry_time):
            return {"msg" : "Token is invalid or expired!"}, 401

        return f(*args, **kwargs)

    return decorated