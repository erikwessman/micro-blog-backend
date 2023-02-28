import json
from db import DBManager
from utils.json_encoder import JSONEncoder
from flask import request, Blueprint
from bson import ObjectId

article_bp = Blueprint('article_route', __name__,
                       url_prefix='/api/article', template_folder='templates')
article_db = DBManager.get_db()['articles']


@article_bp.route("/all", methods=["GET"])
def get_articles():
    articles = list(article_db.find())
    articles_json = JSONEncoder().encode(articles)

    return articles_json, 200


@article_bp.route("", methods=["GET"])
def get_article():
    article_id = request.args['id']
    article = article_db.find_one({"_id": ObjectId(article_id)})
    article_json = JSONEncoder().encode(article)

    return article_json, 200


@article_bp.route("", methods=["POST"])
def create_article():
    article_json = request.data
    article = json.loads(article_json)

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/dummy", methods=["POST"])
def create_article_dummy():
    f = open("src/dummy_data/article.json")
    article = json.load(f)
    f.close()

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("", methods=["PATCH"])
def patch_article():
    article_json = request.data
    article = json.loads(article_json)
    article_id = request.args['id']

    article_db.update_one({"_id": ObjectId(article_id)},
                          {"$set": article})
    return "OK", 200


@article_bp.route("", methods=["DELETE"])
def delete_article():
    article_id = request.args['id']
    article_db.delete_one({"_id": ObjectId(article_id)})

    return "OK", 200


@article_bp.route("/all", methods=["DELETE"])
def delete_articles():
    article_db.delete_many({})

    return "OK", 200
