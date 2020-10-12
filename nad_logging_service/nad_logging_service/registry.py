# TODO FHC
# The registry app is used to track registered applications.

from flask import Flask, Blueprint, request, make_response, abort, current_app
from .auth import generate_token
from .db import app_registry

bp = Blueprint("registry", __name__, url_prefix="/registry")


def init(app: Flask):
    """ This is called during app creation to initialize the registry app. """

    pass


@bp.route("/")
def index():
    return {"applications": list(app_registry.keys())}


@bp.route("/register", methods=["POST"])
def register():
    """ This is a simple view registers an application and produces a token. """
    json = request.json

    if "app_name" not in json:
        abort(400)

    app_name = json["app_name"]

    register_app(app_name)
    token = app_registry[app_name]

    response = make_response(
        {
            "message": f"Application '{app_name}' registered successfully.",
            "token": token,
        },
        201,
    )

    return response


def register_app(app_name):
    """ This function adds an application to the registry. """

    # TODO Add DB
    token = generate_token()
    app_registry[app_name] = token

    current_app.logger.info(f"Application '{request.json['app_name']}' registered.")
