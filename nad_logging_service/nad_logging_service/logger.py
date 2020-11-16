# TODO FHC
# This is the logging service.

import json as _json
import logging
import os
import time
from datetime import datetime
from functools import wraps
from logging.config import dictConfig

from attr import attrib, attrs, validators
from dateutil.parser import isoparse, parse
from flask import Blueprint, Flask, abort, current_app, make_response, request

from .auth import authenticate
from .rate_limiter import limiter

bp = Blueprint("logger", __name__, url_prefix="/logger")

# limiter.limit("5 per minute")(bp)

# ............. Model ............


@attrs(frozen=True)
class LogRecord:

    message: str = attrib()

    log_level: str = attrib()

    @log_level.validator
    def _validate_log_level(self, attribute, value):
        if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            # TODO use validate method instead of throwing error?
            raise ValueError("Invalid log level: " + value)

    application_name: str = attrib()

    process_name: str = attrib()

    process_id: int = attrib(validator=validators.instance_of(int), converter=int)

    client_time: str = attrib()

    @client_time.validator
    def _validate_client_time(self, attribute, value):
        isoparse(value)

    extra: dict = attrib(factory=dict)

    @extra.validator
    def _validate_extra(self, attribute, value):
        if isinstance(value, dict):
            return

        _json.loads(value)

    @classmethod
    def from_json(cls, json):
        message = json["message"]

        application_name = json["applicationName"]
        process_name = json["processName"]
        process_id = json["processId"]
        log_level = json["logLevel"]
        client_time = json["dateTime"]
        extra = json["extra"] if "extra" in json else dict()

        return cls(
            message=message,
            application_name=application_name,
            process_name=process_name,
            process_id=process_id,
            log_level=log_level,
            client_time=client_time,
            extra=extra,
        )


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

# ............. Flask ............


def init(app: Flask):
    """ This is called during app creation to initialize the logger app. """
    LOG_FOLDER = app.config["LOG_FOLDER"]

    # Ensure Logging folder exists
    if not os.path.exists(LOG_FOLDER):
        os.mkdir(LOG_FOLDER)

    # Import Config.
    dictConfig(app.config["LOGGER_CONFIG"])

    # Use UTC time when logging.
    logging.Formatter.converter = time.gmtime

    # Add local logger to rate limiter
    for handler in get_local_logger().handlers:
        limiter.logger.addHandler(handler)


# ............. Functions ............


def get_logger():
    return logging.getLogger(current_app.config["LOGGER_NAME"])


def get_local_logger():
    return logging.getLogger("werkzeug")


def log_record_from_json(json):

    log_record = LogRecord.from_json(json)
    print(log_record)

    return log_record


def valid_log_record(json):
    try:
        LogRecord.from_json(json)

        return True
    except ValueError:

        return False


def write_to_log(log_record):
    message = log_record.message

    extra = {
        "application_name": log_record.application_name,
        "process_name": log_record.process_name,
        "process_id": log_record.process_id,
        "log_level": log_record.log_level,
        # TODO move format string to config file or use the one in logger
        "client_time": isoparse(log_record.client_time).strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ..Add extra properties
    serialized_props = _json.dumps(log_record.extra)
    message += " " + serialized_props

    get_logger().info(message, extra=extra)


# .............. Routes ..............


@bp.route("/")
@limiter.limit("5 per minute")
def index():
    return "Hello World!"


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
            "dateTime",
        ]
        if any(x not in json for x in required_params):
            error_message = "missing required params."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 400)

        if not valid_log_record(json):
            error_message = "invalid log record."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 400)

        log_record = log_record_from_json(json)
        write_to_log(log_record)

        return "Success!"

    return ""
