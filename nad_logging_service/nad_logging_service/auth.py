"""
 * Project Name: NAD-Logging-Service
 * File Name: $auth.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains the authentication app.
"""

# The auth app is used to generate and verify tokens.

import secrets
from functools import wraps

from flask import Blueprint, Flask, abort, current_app, make_response, request

bp = Blueprint("auth", __name__, url_prefix="/auth")


def init(app: Flask):
    """ This is called during app creation to initialize the auth app. """

    if "TOKEN" not in app.config:
        raise RuntimeError("Auth Token is not set!")


def generate_token():
    return secrets.token_urlsafe(16)


def verify_token(token):
    return token == current_app.config["TOKEN"]


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "x-access-token" not in request.headers:
            error_message = "Missing auth token."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 401)

        token = request.headers["x-access-token"]
        if not verify_token(token):
            error_message = "Auth failed."
            current_app.logger.info(error_message)
            return make_response({"message": error_message}, 401)

        return f(*args, **kwargs)

    return decorated_function
