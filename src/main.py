from controllers.authorization import authorization_bp
from controllers.user import user_bp
from controllers.article import article_bp
from controllers.comment import comment_bp
from flask_cors import CORS
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app and connect routes/Blueprints
app = Flask(__name__)
app.register_blueprint(article_bp)
app.register_blueprint(user_bp)
app.register_blueprint(authorization_bp)
app.register_blueprint(comment_bp)

# Enable CORS
CORS(app)


@app.route("/")
def start():
    return "OK", 200


@app.route("/api/status")
def get_status():
    return "Your server is running", 200
