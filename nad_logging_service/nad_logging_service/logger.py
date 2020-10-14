# TODO FHC
# This is the logging service.

import os
from logging.config import dictConfig
from functools import wraps
from flask import (
    Blueprint,
    request,
    Flask,
    current_app,
    abort,
    make_response,
)
from .auth import verify_token

bp = Blueprint("logger", __name__, url_prefix="/logger")

"""
Sample Log:
    {
        "message": "User could not be found.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "ERROR",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime("2020-04-20"),
    },
"""


def init(app: Flask):
    """ This is called during app creation to initialize the logger app. """
    LOG_FOLDER = app.config["LOG_FOLDER"]

    # Ensure Logging folder exists
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)

    # Import Config.
    dictConfig(app.config["LOGGER_CONFIG"])


@bp.route("/")
def index():
    return "Hello World!"


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "x-access-token" not in request.headers:
            error_message = "Missing auth token."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 401)

        token = request.headers["x-access-token"]
        if not verify_token(token):
            error_message = "Auth failed."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 401)

        return f(*args, **kwargs)

    return decorated_function


@bp.route("/log", methods=["GET", "POST"])
@authenticate
def log():
    """ This is a simple view that writes to a log file. """
    if request.method == "POST":
        json = request.json

        if "message" not in json:
            abort(400)

        message = json["message"]

        current_app.logger.info(message)

        return "Success!"

    return ""
