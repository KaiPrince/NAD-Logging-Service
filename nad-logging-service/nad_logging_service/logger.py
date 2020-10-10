# TODO FHC
# This is the logging service.

import os
import logging
from flask import Blueprint, request, Flask

bp = Blueprint("logger", __name__)

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

    log_file_name = "log.log"
    log_file = os.path.join(LOG_FOLDER, log_file_name)

    # Set up logger
    logger = logging.getLogger("file_logger")
    file_handler = logging.FileHandler(log_file)
    logger.addHandler(file_handler)


@bp.route("/")
def index():
    return "Hello World!"


@bp.route("/log", methods=["GET", "POST"])
def log():
    """ This is a simple view that writes to a log file. """
    if request.method == "POST":
        json = request.json
        # TODO: change filename
        message = json["message"]

        logger = logging.getLogger("file_logger")  # TODO move this to config?
        logger.error(message)

        return "Success!"

    return ""
