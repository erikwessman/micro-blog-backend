import json
from db import DBManager
from flask import request, Blueprint, jsonify, current_app
import jwt
import datetime

authorization_bp = Blueprint('authorization_route', __name__,
                             url_prefix='/api/authorization', template_folder='templates')
user_db = DBManager.get_db()['users']


@authorization_bp.route("/login", methods=["GET"])
def login():
    if 'username' in request.args and 'password' in request.args:
        username = request.args['username']
        password = request.args['password']

        user = user_db.find_one({"username": username})

        if user:
            if user['password'] == password:
                token = generate_jwt(username)
                return jsonify({'token': token}), 200
            else:
                return "Password does not match", 400
        else:
            return "User does not exist", 400
    else:
        return "Username or password not specified in request", 400


@authorization_bp.route("/register", methods=["POST"])
def register():
    user_json = request.data
    user = json.loads(user_json)

    if 'username' in user and 'email' in user:
        username = user['username']
        email = user['email']

        if user_db.count_documents({'username': username}, limit=1) != 0:
            return "Username already in use", 400

        if user_db.count_documents({'email': email}, limit=1) != 0:
            return "Email already in use", 400

        user_db.insert_one(user)

        token = generate_jwt(username)
        return jsonify({'token': token}), 200
    else:
        return "Username or email not specified in request", 400


def generate_jwt(username):
    return jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
