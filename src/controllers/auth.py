from flask import request, Blueprint, jsonify
from jsonschema import validate, ValidationError
from src.db import DBManager
from src.validators.user_validator import user_schema, user_login_schema
import src.utils as utils
import bcrypt
import json

auth_bp = Blueprint('authorization_route', __name__,
                    url_prefix='/api/auth', template_folder='templates')
user_db = DBManager.get_db()['users']


@auth_bp.before_request
def get_latest_db():
    global user_db
    user_db = DBManager.get_db()['users']


@auth_bp.route("/login", methods=["POST"])
def login():
    login = json.loads(request.data)

    try:
        validate(login, user_login_schema)
    except ValidationError as error:
        return error.message, 400

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


@auth_bp.route("/register", methods=["POST"])
def register():
    register = json.loads(request.data)

    try:
        validate(register, user_schema)
    except ValidationError as error:
        return error.message, 400

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


@auth_bp.route("/valid", methods=["GET"])
@utils.token_required
def valid():
    return "Token is valid", 200


@auth_bp.route("/refresh", methods=["POST"])
@utils.token_required
def refresh():
    token = request.headers.get("Authorization")
    payload = utils.decode_jwt(token)
    return utils.generate_jwt(payload)
