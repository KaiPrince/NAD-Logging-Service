"""
 * Project Name: NAD-Logging-Service
 * File Name: config.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains configuration classes.
"""

# Config file for the project.

import os

from flask import Flask

"""
 * Class Name: Config
 * Purpose: This purpose of this class is to contain config values.
"""


class Config(object):
    def __init__(self, app: Flask, overwrite_config: dict = None):

        app_config_file = os.path.join(app.config.root_path, "..", "app.cfg")
        app.config.from_pyfile(app_config_file)

        self.LOG_FOLDER = (
            overwrite_config["LOG_FOLDER"]
            if overwrite_config is not None and "LOG_FOLDER" in overwrite_config
            else app.config["LOG_FOLDER"]
            if "LOG_FOLDER" in app.config
            else os.path.join(app.instance_path, "logs")
        )
        self.LOGGER_NAME = app.config["LOGGER_NAME"]
        self.LOCAL_LOGGER_NAME = "local_logger"  # app.config["LOCAL_LOGGER_NAME"]
        self.LOCAL_LOG_FILENAME = app.config["LOCAL_LOG_FILENAME"]
        self.LOGGER_FILENAME = app.config["LOGGER_FILENAME"]

        logging_config_file = os.path.join(app.config.root_path, "..", "logging.cfg")
        app.config.from_pyfile(logging_config_file)

        self.LOGGING_CONFIG_TEMPLATE: dict = app.config["LOGGING_CONFIG_TEMPLATE"]

        self.TOKEN = os.getenv("TOKEN")
        self.SECRET_KEY = os.getenv("SECRET_KEY")

        if overwrite_config is not None:
            self.from_dict(overwrite_config)

    # Logging config needs to be populated with config values
    @property
    def LOGGER_CONFIG(self):
        if hasattr(self, "__logger_config"):
            return getattr(self, "__logger_config")
        else:
            return _logger_config(
                self.LOGGING_CONFIG_TEMPLATE,
                self.LOG_FOLDER,
                self.LOGGER_NAME,
                self.LOCAL_LOG_FILENAME,
                self.LOGGER_FILENAME,
                self.LOCAL_LOGGER_NAME,
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


"""
 * Function Name: _logger_config
 * Description: This function is used to generate a logging config.
 * Parameters: All from config.
    str: log_folder
    str: logger_name
    str: log_folder
    str: log_folder
 * Returns:
    dict: a logging config.
"""


def _logger_config(
    template: dict,
    log_folder: str,
    logger_name: str,
    local_log_filename: str,
    log_filename: str,
    local_logger_name: str,
):

    config = template.copy()
    config["loggers"][logger_name] = config["loggers"].pop("[logger_name]")
    config["loggers"][local_logger_name] = config["loggers"].pop("[local_logger_name]")
    config["handlers"]["file"]["filename"] = os.path.join(log_folder, log_filename)
    config["handlers"]["local_log"]["filename"] = os.path.join(
        log_folder, local_log_filename
    )

    return config
