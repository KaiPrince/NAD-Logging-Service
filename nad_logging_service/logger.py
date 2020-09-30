# TODO FHC
# This is the logging service.

from flask import Blueprint, request

bp = Blueprint("logger", __name__)


@bp.route("/")
def index():
    return "Hello World!"


@bp.route("/log", methods=["GET", "POST"])
def log():
    """ This is a sample view that echos posted JSON. """
    if request.method == "POST":
        return request.json

    return ""
