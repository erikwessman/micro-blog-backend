from flask import Blueprint

app_bp = Blueprint('app_route', __name__, url_prefix="",
                   template_folder='templates')


@app_bp.route("/")
def start():
    return "OK", 200


@app_bp.route("/api/status")
def get_status():
    return "Your server is running", 200
