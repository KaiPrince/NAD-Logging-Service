"""
 * Project Name: NAD-Logging-Service
 * File Name: conftest.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains test setup.
"""


import os

import pytest

from nad_logging_service import create_app
from nad_logging_service.utils import copyfile

LOG_FOLDER = os.path.join(os.path.curdir, "tests", "logs")


@pytest.fixture
def app(tmp_path):
    temp_logs_folder = tmp_path

    # Copy files in test logs folder to temp directory
    filesToCopy = os.listdir(LOG_FOLDER)
    for f in filesToCopy:
        with open(os.path.join(LOG_FOLDER, f), "rb") as src:
            dest_file = temp_logs_folder / f
            copyfile(src, dest_file)

    TEST_CONFIG = {
        "TESTING": True,
        "LOG_FOLDER": temp_logs_folder,
        "TOKEN": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        # TODO enable rate limiting only on certain tests
        # "RATELIMIT_ENABLED": False,
    }

    app = create_app(TEST_CONFIG)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
