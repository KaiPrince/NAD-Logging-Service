"""
* Project Name: NAD-Logging_Service
* File Name: __init__.py
* Programmer: Kai Prince
* Date: Sun, Sept 27, 2020
* Description: This file contains the main entry point for the app.
"""

import os
from flask import Flask
from flask_cors import CORS
from . import logger, config, auth


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    # CORS policy
    # TODO: specify allowed origins
    CORS(app)  # TEMP allow all.

    # load config
    config_obj = config.Config(app)
    app.config.from_object(config_obj)

    if test_config is not None:
        # merge the test config if passed in
        app.config.from_mapping(test_config)

    # make sure instance folder exists.
    if not os.path.exists(app.instance_path):
        os.mkdir(app.instance_path)

    # register routes
    app.register_blueprint(logger.bp)
    app.register_blueprint(auth.bp)

    # initialize apps
    logger.init(app)
    auth.init(app)

    app.add_url_rule("/", "index", logger.index)

    return app
