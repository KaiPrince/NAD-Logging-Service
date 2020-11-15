# TODO File Header comment
# Config file for the project.

import os
from flask import Flask


class Config(object):
    LOGGER_NAME = "logger"
    LOGGER_FILENAME = "log.log"

    LOCAL_LOG_FILENAME = "local.log"

    RATELIMIT_DEFAULT = "1 per second"

    def __init__(self, app: Flask, overwrite_config: dict = None):

        self.LOG_FOLDER = os.path.join(app.instance_path, "logs")

        if overwrite_config is not None:
            self.from_dict(overwrite_config)

    # TODO find out what this does and comment it
    @property
    def LOGGER_CONFIG(self):
        if hasattr(self, "__logger_config"):
            return getattr(self, "__logger_config")
        else:
            return _logger_config(
                self.LOG_FOLDER,
                self.LOGGER_NAME,
                self.LOCAL_LOG_FILENAME,
                self.LOGGER_FILENAME,
            )

    @LOGGER_CONFIG.setter
    def LOGGER_CONFIG(self, val):
        self.__logger_config = val

    def from_dict(self, obj):
        """Merge keys into this object. (Uppercase keys only)"""
        for key in obj:
            if key.isupper():
                value = obj[key]
                setattr(self, key, value)


def _logger_config(
    log_folder: str, logger_name: str, local_log_filename: str, log_filename: str
):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "brief": {"format": "%(message)s"},
            "default": {
                "format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "logger": {
                "format": "%(asctime)s %(log_level)-8s "
                "%(application_name)-10s:%(process_name)-5s:%(process_id)-5s "
                "%(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "loggers": {
            logger_name: {
                "handlers": ["file"],
                "level": "INFO",
                "formatter": "logger",
            },
            "werkzeug": {
                "handlers": ["local_log"],
                "level": "DEBUG",
            },
        },
        "handlers": {
            # "console": {
            #     "class": "logging.StreamHandler",
            #     "level": "DEBUG",
            #     "formatter": "brief",
            #     "stream": "ext://sys.stdout",
            # },
            "file": {
                "class": "logging.FileHandler",
                "level": "INFO",
                "formatter": "logger",
                "filename": os.path.join(log_folder, log_filename),
            },
            "local_log": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "default",
                "filename": os.path.join(log_folder, local_log_filename),
            }
            # "wsgi": {
            #     "class": "logging.StreamHandler",
            #     "stream": "ext://flask.logging.wsgi_errors_stream",
            #     "formatter": "default",
            # },
        },
        "root": {"level": "INFO", "handlers": []},
    }