# TODO FHC
# This is the logging service.

from flask import Blueprint

bp = Blueprint("logger", __name__)


@bp.route("/")
def index():
    return "Hello World!"
