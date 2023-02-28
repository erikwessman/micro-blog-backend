from flask import Flask
from flask_cors import CORS
from controllers.article import article_bp

# Create Flask app and connect routes/Blueprints
app = Flask(__name__)
CORS(app)
app.register_blueprint(article_bp)


@app.route("/")
def start():
    return "OK", 200


@app.route("/api/status")
def get_status():
    return "Your server is running", 200
