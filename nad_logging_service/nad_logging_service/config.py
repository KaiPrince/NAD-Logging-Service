# TODO File Header comment
# Config file for the project.

import os
from flask import Flask


class Config(object):
    def __init__(self, app: Flask):

        self.LOG_FOLDER = os.path.join(app.instance_path, "logs")
