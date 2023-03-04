import json
from db import DBManager
from utils.json_encoder import JSONEncoder
from flask import request, Blueprint
from bson import ObjectId

user_bp = Blueprint('user_route', __name__,
                    url_prefix='api/user', template_folder='templates')
user_db = DBManager.get_db()['users']


@user_bp.route("", methods=["GET"])
def login():
    return "OK", 200


@user_bp.route("", methods=["GET"])
def get_user():
    user = None

    if request.args.getlist('id'):
        user_id = request.args['id']
        user = user_db.find_one({"_id": ObjectId(user_id)})
    else:
        user = list(user_db.find(request.args))

    user_json = JSONEncoder().encode(user)
    return user_json, 200


@user_bp.route("", methods=["POST"])
def create_user():
    user_json = request.data
    user = json.loads(user_json)

    user_insert = user_db.insert_one(user)
    user_id = str(user_insert.inserted_id)

    return user_id, 200


@user_bp.route("/dummy", methods=["POST"])
def create_user_dummy():
    f = open("src/dummy_data/user.json")
    user = json.load(f)
    f.close()

    user_insert = user_db.insert_one(user)
    user_id = str(user_insert.inserted_id)

    return user_id, 200


@user_bp.route("", methods=["PATCH"])
def patch_user():
    user_json = request.data
    user = json.loads(user_json)
    user_id = request.args['id']

    user_db.update_one({"_id": ObjectId(user_id)},
                       {"$set": user})
    return "OK", 200


@user_bp.route("", methods=["DELETE"])
def delete_user():
    if request.args:
        user_id = request.args['id']
        user_db.delete_one({"_id": ObjectId(user_id)})
    else:
        user_db.delete_many({})

    return "OK", 200