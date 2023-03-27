from flask import request, Blueprint
from jsonschema import validate, ValidationError
from src.db import DBManager
from bson import ObjectId
from src.validators.article_validators import article_schema, article_user_schema
import src.utils as utils
import json

article_bp = Blueprint('article_route', __name__,
                       url_prefix='/api/article', template_folder='templates')
article_db = DBManager.get_db()['articles']


@article_bp.route("", methods=["GET"])
def get_article():
    article = None

    if 'id' in request.args:
        article_id = request.args['id']
        article = article_db.find_one({"_id": ObjectId(article_id)})
    else:
        filter_dict = utils.build_article_filter(request.args.to_dict())
        pagination_dict = utils.build_pagination(
            request.args.to_dict())

        article = list(article_db.find(filter_dict)
                       .sort('date', -1)
                       .skip(pagination_dict['skip'])
                       .limit(pagination_dict['limit']))

    if article is not None:
        article_json = utils.JSONEncoder().encode(article)
        return article_json, 200
    else:
        return "Not found", 404


@article_bp.route("", methods=["POST"])
@utils.admin_required
def create_article():
    article = json.loads(request.data)

    try:
        validate(article, article_schema)
    except ValidationError as error:
        return error.message, 400

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/user", methods=["POST"])
@utils.token_required
def create_article_user():
    article = json.loads(request.data)

    try:
        validate(article, article_user_schema)
    except ValidationError as error:
        return error.message, 400

    token = request.headers.get('Authorization')
    data = utils.decode_jwt(token)
    username = data['username']

    article['author'] = username
    article['date'] = utils.get_utc_timestamp_now()

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("", methods=["PATCH"])
@utils.admin_required
def patch_article():
    article = json.loads(request.data)

    if 'id' in request.args:
        article_id = request.args['id']
        article_db.update_one({"_id": ObjectId(article_id)},
                              {"$set": article})
        return "OK", 200
    else:
        return "ID not specified in request", 400


@article_bp.route("", methods=["DELETE"])
@utils.admin_required
def delete_article():
    if 'id' in request.args:
        article_id = request.args['id']
        article_db.delete_one({"_id": ObjectId(article_id)})
    else:
        article_db.delete_many({})

    return "OK", 200
