"""
* Project Name: NAD-Logging_Service
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Sept 27, 2020
* Description: This file contains the main entry point for the app.
"""

import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS

from . import auth, config, logger
from .rate_limiter import limiter

load_dotenv(find_dotenv(), verbose=True)


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)

    # CORS policy
    # TODO: specify allowed origins
    CORS(app)  # TEMP allow all.

    # load config
    config_obj = config.Config(app, test_config)
    app.config.from_object(config_obj)

    # make sure instance folder exists.
    if not os.path.exists(app.instance_path):
        os.mkdir(app.instance_path)

    # initialize apps
    logger.init(app)
    auth.init(app)
    limiter.init_app(app)

    # register routes
    app.register_blueprint(logger.bp)
    app.register_blueprint(auth.bp)
    app.add_url_rule("/", "index", logger.index)

    return app
