from flask import Flask
from flask_cors import CORS
from controllers.article import article_bp
from controllers.user import user_bp

# Create Flask app and connect routes/Blueprints
app = Flask(__name__)
app.register_blueprint(article_bp)
app.register_blueprint(user_bp)

# Enable CORS
CORS(app)

# Set config for JWT
app.config['SECRET_KEY'] = 'eriks_key'


@app.route("/")
def start():
    return "OK", 200


@app.route("/api/status")
def get_status():
    return "Your server is running", 200
