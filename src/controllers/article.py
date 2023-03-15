from flask import request, Blueprint
from utils import JSONEncoder, decode_jwt, token_required, admin_required, get_utc_timestamp_now, build_article_filter
from db import DBManager
from bson import ObjectId
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
        article_filter = build_article_filter(request.args.to_dict())
        article = list(article_db.find(article_filter))
        article.sort(key=lambda x: x['date'], reverse=True)

    article_json = JSONEncoder().encode(article)
    return article_json, 200


@article_bp.route("", methods=["POST"])
@admin_required
def create_article():
    article = json.loads(request.data)

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/user", methods=["POST"])
@token_required
def create_article_user():
    article = json.loads(request.data)

    token = request.headers.get('Authorization')
    data = decode_jwt(token)
    username = data['username']

    article['author'] = username
    article['date'] = get_utc_timestamp_now()

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/dummy", methods=["POST"])
@admin_required
def create_article_dummy():
    f = open("src/dummy_data/article.json")
    article = json.load(f)
    f.close()

    article['date'] = get_utc_timestamp_now()

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("", methods=["PATCH"])
@admin_required
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
@admin_required
def delete_article():
    if 'id' in request.args:
        article_id = request.args['id']
        article_db.delete_one({"_id": ObjectId(article_id)})
    else:
        article_db.delete_many({})

    return "OK", 200
