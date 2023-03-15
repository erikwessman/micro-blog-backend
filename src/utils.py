from flask import request
from functools import wraps
from bson import ObjectId
from os import getenv
from datetime import timezone
import datetime
import jwt
import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (ObjectId, bytes, bytearray)):
            return str(o)
        return json.JSONEncoder.default(self, o)


def generate_jwt(payload, duration=60):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=duration)
    return jwt.encode(payload, getenv("JWT_KEY"))


def decode_jwt(token):
    return jwt.decode(token, getenv("JWT_KEY"), algorithms=["HS256"])


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

        if admin_key != getenv("ADMIN_KEY"):
            return "Admin key is incorrect", 403

        return f(*args, **kwargs)

    return decorated


def get_utc_timestamp():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return utc_time.timestamp()
