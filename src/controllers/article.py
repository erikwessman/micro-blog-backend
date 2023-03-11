import json
from db import DBManager
from utils.json_encoder import JSONEncoder
from flask import request, Blueprint, current_app
from bson import ObjectId
import jwt
import datetime

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
        article = list(article_db.find(request.args))
        article.sort(key=lambda x: datetime.datetime.strptime(x['date'], '%d-%m-%Y'), reverse=True)

    article_json = JSONEncoder().encode(article)
    return article_json, 200


@article_bp.route("", methods=["POST"])
def create_article():
    article_json = request.data
    article = json.loads(article_json)

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/user", methods=["POST"])
def create_article_user():
    article_json = request.data
    article = json.loads(article_json)
    
    token = request.headers.get('Authorization')
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    username = data['username']

    article['author'] = username
    article['date'] = datetime.datetime.today().strftime('%d-%m-%Y')

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("/dummy", methods=["POST"])
def create_article_dummy():
    f = open("src/dummy_data/article.json")
    article = json.load(f)
    f.close()

    article['date'] = datetime.datetime.today().strftime('%d-%m-%Y')

    article_insert = article_db.insert_one(article)
    article_id = str(article_insert.inserted_id)

    return article_id, 200


@article_bp.route("", methods=["PATCH"])
def patch_article():
    article_json = request.data
    article = json.loads(article_json)

    if 'id' in request.args:
        article_id = request.args['id']
        article_db.update_one({"_id": ObjectId(article_id)},
                              {"$set": article})
        return "OK", 200
    else:
        return "ID not specified in request", 400


@article_bp.route("", methods=["DELETE"])
def delete_article():
    if 'id' in request.args:
        article_id = request.args['id']
        article_db.delete_one({"_id": ObjectId(article_id)})
    else:
        article_db.delete_many({})

    return "OK", 200
