from flask import request, current_app
from functools import wraps
from bson import ObjectId
import datetime
import jwt
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def generate_jwt(payload, duration=60):
    payload['exp'] = datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=duration)
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


def decode_jwt(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return "Token is missing", 403

        try:
            decode_jwt(token)
        except:
            return "Token is invalid", 403

        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        admin_key = request.headers.get('Authorization')

        if not admin_key:
            return "Admin key is missing", 403

        if admin_key != '123':
            return "Admin key is incorrect", 403

        return f(*args, **kwargs)

    return decorated
