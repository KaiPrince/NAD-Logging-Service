"""
 * Project Name: NAD-Logging-Service
 * File Name: logger.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains the logging app.
"""


import json as _json
import logging
import os
import time
from logging.config import dictConfig

from attr import attrib, attrs, validators
from dateutil.parser import isoparse
from flask import Blueprint, Flask, current_app, make_response, request

from .auth import authenticate
from .rate_limiter import limiter

bp = Blueprint("logger", __name__, url_prefix="/logger")

# ............. Model ............


@attrs(frozen=True)
class LogRecord:

    message: str = attrib()

    log_level: str = attrib()

    @log_level.validator
    def _validate_log_level(self, attribute, value):
        if value not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log level: " + value)

    application_name: str = attrib()

    process_name: str = attrib()

    process_id: int = attrib(validator=validators.instance_of(int), converter=int)

    client_time: str = attrib()

    @client_time.validator
    def _validate_client_time(self, attribute, value):
        try:
            isoparse(value)
        except Exception:
            raise ValueError("Improper date format " + value)

    extra: dict = attrib(factory=dict)

    @extra.validator
    def _validate_extra(self, attribute, value):
        if isinstance(value, dict):
            return

        try:
            _json.loads(value)
        except Exception as e:
            raise ValueError("Improper json format. " + str(e))

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

"""
 * Function Name: init
 * Description: This function is used to initialize the logging service.
 * Parameters:
    Flask: app
 * Returns: None
"""


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
    with app.app_context():
        local_logger = get_local_logger()
        for handler in local_logger.handlers:
            limiter.logger.addHandler(handler)

        # NOTE: for some reason, this is originally the string "False",
        #   which is truthy. Without this line, the logger does not work.
        limiter.logger.disabled = False


# ............. Functions ............


def get_logger():
    return logging.getLogger(current_app.config["LOGGER_NAME"])


def get_local_logger():
    return logging.getLogger(current_app.config["LOCAL_LOGGER_NAME"])


def log_record_from_json(json):

    log_record = LogRecord.from_json(json)

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
    """
    * Function Name: log
    * Description: This is a simple view that writes to a log file.
    * Parameters: None
    * Returns: None
    """
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
            try:
                LogRecord.from_json(json)
            except Exception as e:
                error_message = "invalid log record: " + str(e)
                current_app.logger.info(error_message)
                return make_response({"message": error_message}, 400)

        log_record = log_record_from_json(json)
        write_to_log(log_record)

        return "Success!"

    return ""
