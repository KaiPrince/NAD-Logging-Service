# TODO FHC
# This is the logging service.

import os
from flask import Blueprint, request, current_app, Flask

bp = Blueprint("logger", __name__)


def init(app: Flask):

    # Ensure Logging folder exists
    if os.path.exists(app.config["LOG_FOLDER"]):
        os.mkdir(app.config["LOG_FOLDER"])


@bp.route("/")
def index():
    return "Hello World!"


@bp.route("/log", methods=["GET", "POST"])
def log():
    """ This is a simple view that writes to a log file. """
    if request.method == "POST":
        json = request.json
        # TODO: change filename
        logfile_name = json["filename"] if "filename" in json else "log.log"
        message = json["message"]

        logfile_path = current_app.config["LOG_FOLDER"]
        logfile = os.path.join(logfile_path, logfile_name)

        with open(logfile, "w+") as f:
            f.write(message)

        return "Success!"

    return ""
