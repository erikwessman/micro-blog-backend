from flask import request, Blueprint
from db import DBManager
from bson import ObjectId
from utils import admin_required, token_required, get_utc_timestamp_now, decode_jwt, JSONEncoder
import json

comment_bp = Blueprint('comment_route', __name__,
                       url_prefix='/api/comment', template_folder='templates')
comment_db = DBManager.get_db()['comments']


@comment_bp.route("", methods=["GET"])
def get_comment():
    comment = None

    if 'id' in request.args:
        comment_id = request.args['id']
        comment = comment_db.find_one({"_id": ObjectId(comment_id)})
    elif 'article_id' in request.args:
        article_id = request.args['article_id']
        comment = comment_db.find_one({"article_id": article_id})
    else:
        comment = list(comment_db.find({}))

    if comment:
        comment_json = JSONEncoder().encode(comment)
        return comment_json, 200
    else:
        return "Not found", 404


@comment_bp.route("", methods=["POST"])
@admin_required
def create_comment():
    comment = json.loads(request.data)

    comment_insert = comment_db.insert_one(comment)
    comment_id = str(comment_insert.inserted_id)

    return comment_id, 200


@comment_bp.route("/user", methods=["POST"])
@token_required
def create_comment_user():
    comment = json.loads(request.data)

    token = request.headers.get('Authorization')
    data = decode_jwt(token)
    username = data['username']

    comment['author'] = username
    comment['date'] = get_utc_timestamp_now()

    comment_insert = comment_db.insert_one(comment)
    comment_id = str(comment_insert.inserted_id)

    return comment_id, 200


@comment_bp.route("", methods=["PATCH"])
@admin_required
def patch_comment():
    comment = json.loads(request.data)

    if 'id' in request.args:
        comment_id = request.args['id']
        comment_db.update_one({"_id": ObjectId(comment_id)},
                              {"$set": comment})
        return "OK", 200
    else:
        return "ID not specified in request", 400


@comment_bp.route("", methods=["DELETE"])
@admin_required
def delete_comment():
    if 'id' in request.args:
        comment_id = request.args['id']
        comment_db.delete_one({"_id": ObjectId(comment_id)})
    else:
        comment_db.delete_many({})

    return "OK", 200
