from flask import request, Blueprint
from jsonschema import validate, ValidationError
from src.db import DBManager
from bson import ObjectId
from src.validators.comment_validators import comment_schema, comment_user_schema
import src.utils as utils
import json

comment_bp = Blueprint('comment_route', __name__,
                       url_prefix='/api/comment', template_folder='templates')
comment_db = DBManager.get_db()['comments']


@comment_bp.before_request
def get_latest_db():
    global comment_db
    comment_db = DBManager.get_db()['comments']


@comment_bp.route("", methods=["GET"])
def get_comment():
    comment = None

    if 'id' in request.args:
        comment_id = request.args['id']
        comment = comment_db.find_one({"_id": ObjectId(comment_id)})
    elif 'article_id' in request.args:
        article_id = request.args['article_id']
        pagination_dict = utils.build_pagination(request.args.to_dict())

        comment = list(comment_db.find({"article_id": article_id})
                       .sort('date', -1)
                       .skip(pagination_dict['skip'])
                       .limit(pagination_dict['limit']))

    else:
        comment = list(comment_db.find({}))

    if comment is not None:
        comment_json = utils.JSONEncoder().encode(comment)
        return comment_json, 200
    else:
        return "Not found", 404


@comment_bp.route("", methods=["POST"])
@utils.admin_required
def create_comment():
    comment = json.loads(request.data)

    try:
        validate(comment, comment_schema)
    except ValidationError as error:
        return error.message, 400

    comment_insert = comment_db.insert_one(comment)
    comment_id = str(comment_insert.inserted_id)

    return comment_id, 200


@comment_bp.route("/user", methods=["POST"])
@utils.token_required
def create_comment_user():
    comment = json.loads(request.data)

    token = request.headers.get('Authorization')
    data = utils.decode_jwt(token)
    username = data['username']

    comment['author'] = username
    comment['date'] = utils.get_utc_timestamp_now()

    try:
        validate(comment, comment_user_schema)
    except ValidationError as error:
        return error.message, 400

    comment_insert = comment_db.insert_one(comment)
    comment_id = str(comment_insert.inserted_id)

    return comment_id, 200


@comment_bp.route("", methods=["PATCH"])
@utils.admin_required
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
@utils.admin_required
def delete_comment():
    if 'id' in request.args:
        comment_id = request.args['id']
        comment_db.delete_one({"_id": ObjectId(comment_id)})
    else:
        comment_db.delete_many({})

    return "OK", 200
