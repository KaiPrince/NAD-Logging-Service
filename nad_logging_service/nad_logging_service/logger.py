# TODO FHC
# This is the logging service.

import os
from logging.config import dictConfig
import logging
import json as _json
from functools import wraps
from flask import Blueprint, request, Flask, current_app, abort, make_response
from .auth import verify_token
from .rate_limiter import limiter

bp = Blueprint("logger", __name__, url_prefix="/logger")

# limiter.limit("5 per minute")(bp)

"""
Sample Log:
    {
        "message": "User could not be found.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "ERROR",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime("2020-04-20"),
        "processName": "node.exe"
        "processId": 6545,
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


def get_logger():
    return logging.getLogger(current_app.config["LOGGER_NAME"])


@bp.route("/")
@limiter.limit("5 per minute")
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

        required_params = [
            "message",
            "applicationName",
            "processName",
            "processId",
            "logLevel",
        ]
        if any(x not in json for x in required_params):
            return abort(400)

        application_name = json["applicationName"]
        message = json["message"]
        process_name = json["processName"]
        process_id = json["processId"]
        log_level = json["logLevel"]

        extra = {
            "application_name": application_name,
            "process_name": process_name,
            "process_id": process_id,
            "log_level": log_level,
        }

        # ..Add extra properties
        if "extra" in json:
            serialized_props = _json.dumps(json["extra"])
            message += " " + serialized_props

        get_logger().info(message, extra=extra)

        return "Success!"

    return ""
