# TODO FHC
# The registry app is used to track registered applications.

from flask import Flask, Blueprint, request, make_response, abort, current_app
from .auth import generate_token
from .db import get_db

bp = Blueprint("registry", __name__, url_prefix="/registry")


def init(app: Flask):
    """ This is called during app creation to initialize the registry app. """

    pass


@bp.route("/", methods=["POST", "DELETE"])
def index():
    """ This is a simple view registers an application and produces a token. """
    db = get_db()

    if request.method == "POST":
        json = request.json

        if "app_name" not in json:
            abort(400)

        app_name = json["app_name"]

        register_app(app_name)
        token = db[app_name]  # TODO change when implementing DB

        response = make_response(
            {
                "message": f"Application '{app_name}' registered successfully.",
                "token": token,
            },
            201,
        )
        return response

    elif request.method == "DELETE":
        return "NOT IMPLEMENTED"  # TODO


def register_app(app_name):
    """ This function adds an application to the registry. """

    token = generate_token()
    db = get_db()
    db[app_name] = token  # TODO change when implementing DB

    current_app.logger.info(f"Application '{request.json['app_name']}' registered.")
