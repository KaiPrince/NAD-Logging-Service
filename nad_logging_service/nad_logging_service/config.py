# TODO File Header comment
# Config file for the project.

import os
from flask import Flask


class Config(object):
    def __init__(self, app: Flask):

        self.LOG_FOLDER = os.path.join(app.instance_path, "logs")
        self.LOGGER_CONFIG = {
            "version": 1,
            "formatters": {
                "brief": {"format": "%(message)s"},
                "default": {
                    "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "brief",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "default",
                    "filename": os.path.join(self.LOG_FOLDER, "log.log"),
                },
                # "wsgi": {
                #     "class": "logging.StreamHandler",
                #     "stream": "ext://flask.logging.wsgi_errors_stream",
                #     "formatter": "default",
                # },
            },
            "root": {"level": "INFO", "handlers": ["console", "file"]},
        }
