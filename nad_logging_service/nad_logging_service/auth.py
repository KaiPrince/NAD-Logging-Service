# TODO FHC
# The auth app is used to generate and verify tokens.

import secrets
from flask import Flask, Blueprint, request, abort, make_response
from .db import app_registry

bp = Blueprint("auth", __name__, url_prefix="/auth")


def init(app: Flask):
    """ This is called during app creation to initialize the auth app. """

    pass


@bp.route("/token", methods=["POST"])
def token_route():
    """ This view function returns a token for the provided app_name. """
    print("registry", app_registry)

    if "app_name" not in request.json:
        abort(400)

    app_name = request.json["app_name"]

    if app_name not in app_registry:
        abort(404)

    return {"token": app_registry[app_name]}


@bp.route("/verify_token", methods=["POST"])
def verify_token_route():
    """ This view function simply return a status 200 if the token is valid. """

    if "app_name" not in request.json or "token" not in request.json:
        abort(400)

    app_name = request.json["app_name"]
    token = request.json["token"]

    if app_name not in app_registry:
        abort(404)

    if verify_token(token, app_name):
        return make_response({"message": "Token is valid."}, 200)
    else:
        return make_response({"message": "Token is not valid."}, 401)


def generate_token():
    return secrets.token_urlsafe(16)


def verify_token(token, app_name):
    return token == app_registry[app_name]
