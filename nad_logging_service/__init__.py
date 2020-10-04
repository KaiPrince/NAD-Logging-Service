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
from . import logger, config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "web_server.sqlite"),
    )

    # CORS policy
    # TODO: specify allowed origins
    CORS(app)  # TEMP allow all.

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        # TODO: merge config object with test_config
        config_obj = config.Config(app)
        app.config.from_object(config_obj)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register routes
    app.register_blueprint(logger.bp)

    return app
