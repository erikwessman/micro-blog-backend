from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def start():
    return "OK", 200

@app.route("/article", methods=["GET"])
def get_articles():
    f = open("src/test_data/articles.json")
    articles = json.load(f)
    f.close()
    return articles, 200

@app.route("/article<id>", methods=["GET"])
def get_article(id):
    return "OK", 200

@app.route("/article<id>", methods=["PATCH"])
def patch_article(id):
    return "OK", 200

@app.route("/article", methods=["POST"])
def create_articles():
    article = request.data
    return "OK", 200