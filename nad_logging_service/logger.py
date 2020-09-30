# TODO FHC
# This is the logging service.

import os
from flask import Blueprint, request, current_app

bp = Blueprint("logger", __name__)


@bp.route("/")
def index():
    return "Hello World!"


@bp.route("/log", methods=["GET", "POST"])
def log():
    """ This is a simple view that writes to a log file. """
    if request.method == "POST":
        json = request.json
        logfile_name = json["filename"]
        message = json["message"]

        logfile_path = current_app.config["LOG_FOLDER"]
        logfile = os.path.join(logfile_path, logfile_name)

        with open(logfile, "w+") as f:
            f.write(message)

        return "Success!"

    return ""
