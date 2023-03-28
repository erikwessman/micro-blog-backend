from flask import request, Blueprint
from jsonschema import validate, ValidationError
from src.db import DBManager
from bson import ObjectId
from src.validators.user_validator import user_schema
import json
import src.utils as utils

user_bp = Blueprint('user_route', __name__,
                    url_prefix='/api/user', template_folder='templates')
user_db = DBManager.get_db()['users']


@user_bp.before_request
def get_latest_db():
    global user_db
    user_db = DBManager.get_db()['users']


@user_bp.route("", methods=["GET"])
@utils.admin_required
def get_user():
    user = None

    if 'id' in request.args:
        user_id = request.args['id']
        user = user_db.find_one({"_id": ObjectId(user_id)})
    else:
        user = list(user_db.find(request.args))

    if user is not None:
        user_json = utils.JSONEncoder().encode(user)
        return user_json, 200
    else:
        return "Not found", 404


@user_bp.route("", methods=["POST"])
@utils.admin_required
def create_user():
    user = json.loads(request.data)

    try:
        validate(user, user_schema)
    except ValidationError as error:
        return error.message, 400

    user_insert = user_db.insert_one(user)
    user_id = str(user_insert.inserted_id)

    return user_id, 200


@user_bp.route("", methods=["PATCH"])
@utils.admin_required
def patch_user():
    user = json.loads(request.data)

    if 'id' in request.args:
        user_id = request.args['id']
        user_db.update_one({"_id": ObjectId(user_id)},
                           {"$set": user})
        return "OK", 200
    else:
        return "ID not specified in request", 400


@user_bp.route("", methods=["DELETE"])
@utils.admin_required
def delete_user():
    if 'id' in request.args:
        user_id = request.args['id']
        user_db.delete_one({"_id": ObjectId(user_id)})
    else:
        user_db.delete_many({})

    return "OK", 200
