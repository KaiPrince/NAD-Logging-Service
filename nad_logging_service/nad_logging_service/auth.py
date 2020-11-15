"""
 * Project Name: NAD-Logging-Service
 * File Name: $auth.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains the authentication app.
"""

# The auth app is used to generate and verify tokens.

import secrets
from flask import Flask, Blueprint, request, abort, make_response

bp = Blueprint("auth", __name__, url_prefix="/auth")


def init(app: Flask):
    """ This is called during app creation to initialize the auth app. """

    pass


def generate_token():
    return secrets.token_urlsafe(16)


def verify_token(token):
    return True  # token == app_registry[app_name]
