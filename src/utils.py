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


def get_utc_timestamp_now():
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    return utc_time.timestamp()


def get_date_range(date):
    dt = datetime.datetime.strptime(date, '%d/%m/%Y')

    from_date = dt.replace(tzinfo=timezone.utc).timestamp()
    to_date = from_date + 60*60*24

    return from_date, to_date


def build_article_filter(args):
    article_filter = {}

    if 'author' in args:
        article_filter['author'] = args['author']

    if 'categories' in args:
        article_filter['categories'] = args['categories']

    if 'date' in args:
        from_date, to_date = get_date_range(args['date'])
        article_filter['date'] = {
            '$gte': from_date,
            '$lt': to_date
        }

    return article_filter


def build_pagination(args):
    article_pagination = {
        'skip': 0,
        'limit': 1000
    }

    if 'page' in args and 'limit' in args:
        article_pagination['skip'] = int(args['page']) * int(args['limit'])
        article_pagination['limit'] = int(args['limit'])
    elif 'limit' in args:
        article_pagination['limit'] = int(args['limit'])

    return article_pagination
