import json
from db import DBManager
from utils.json_encoder import JSONEncoder
from flask import request, jsonify, Blueprint

article_bp = Blueprint('article_route', __name__, url_prefix='/api/article', template_folder='templates')
article_db = DBManager.get_db()['articles']

@article_bp.route("", methods=["GET"])
def get_articles():
    articles = list(article_db.find())
    articles_json = JSONEncoder().encode(articles)
    return articles_json, 200

@article_bp.route("", methods=["POST"])
def create_articles():
    article_json = request.data
    article = json.loads(article_json)

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)
    return article_id, 200

@article_bp.route("<id>", methods=["GET"])
def get_article(id):
    return "OK", 200

@article_bp.route("<id>", methods=["PATCH"])
def patch_article(id):
    return "OK", 200

@article_bp.route("<id>", methods=["DELETE"])
def delete_article(id):
    return "OK", 200