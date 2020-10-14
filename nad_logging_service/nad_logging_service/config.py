# TODO File Header comment
# Config file for the project.

import os
from flask import Flask


class Config(object):
    def __init__(self, app: Flask, overwrite_config: dict = None):

        self.LOG_FOLDER = os.path.join(app.instance_path, "logs")

        if overwrite_config is not None:
            self.from_dict(overwrite_config)

    @property
    def LOGGER_CONFIG(self):
        if hasattr(self, "__logger_config"):
            return getattr(self, "__logger_config")
        else:
            return _logger_config(self.LOG_FOLDER)

    @LOGGER_CONFIG.setter
    def LOGGER_CONFIG(self, val):
        self.__logger_config = val

    def from_dict(self, obj):
        """Merge keys into this object. (Uppercase keys only)"""
        for key in obj:
            if key.isupper():
                value = obj[key]
                setattr(self, key, value)


def _logger_config(log_folder: str):
    return {
        "version": 1,
        "disable_existing_loggers": False,
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
                "filename": os.path.join(log_folder, "log.log"),
            },
            # "wsgi": {
            #     "class": "logging.StreamHandler",
            #     "stream": "ext://flask.logging.wsgi_errors_stream",
            #     "formatter": "default",
            # },
        },
        "root": {"level": "INFO", "handlers": ["console", "file"]},
    }
