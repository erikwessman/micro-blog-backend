from flask import request, Blueprint, jsonify
import utils
from db import DBManager
import bcrypt
import json

authorization_bp = Blueprint('authorization_route', __name__,
                             url_prefix='/api/authorization', template_folder='templates')
user_db = DBManager.get_db()['users']


@authorization_bp.route("/login", methods=["POST"])
def login():
    login = json.loads(request.data)

    if 'username' in login and 'password' in login:
        username = login['username']
        password = login['password']

        user = user_db.find_one({"username": username})

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                token = utils.generate_jwt({'username': username})
                return jsonify({'token': token}), 200
            else:
                return "Password does not match", 400
        else:
            return "User does not exist", 400
    else:
        return "Username or password not specified in request", 400


@authorization_bp.route("/register", methods=["POST"])
def register():
    register = json.loads(request.data)

    if 'username' in register and 'email' in register:
        username = register['username']
        email = register['email']
        password = register['password']

        if user_db.count_documents({'username': username}, limit=1) != 0:
            return "Username already in use", 400

        if user_db.count_documents({'email': email}, limit=1) != 0:
            return "Email already in use", 400

        # Update the request with hashed password
        register['password'] = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

        user_db.insert_one(register)

        token = utils.generate_jwt({'username': username})
        return jsonify({'token': token}), 200
    else:
        return "Username or email not specified in request", 400


@authorization_bp.route("/valid", methods=["GET"])
@utils.token_required
def valid():
    return "Token is valid", 200


@authorization_bp.route("/refresh", methods=["POST"])
@utils.token_required
def refresh():
    token = request.headers.get("Authorization")
    payload = utils.decode_jwt(token)
    return utils.generate_jwt(payload)
