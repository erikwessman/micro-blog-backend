from flask import Flask
from flask_cors import CORS


def init_app():
    # Create Flask app and connect routes/Blueprints
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    CORS(app)

    with app.app_context():
        from .controllers.app import app_bp
        from .controllers.article import article_bp
        from .controllers.auth import auth_bp
        from .controllers.user import user_bp
        from .controllers.comment import comment_bp

        app.register_blueprint(app_bp)
        app.register_blueprint(article_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(comment_bp)

        return app
