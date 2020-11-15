"""
 * Project Name: NAD-Logging-Service
 * File Name: test_logger.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains tests for the logger app.
"""

import os
import pytest
from datetime import datetime
import json

sample_logs = [
    {
        "message": "The app has crashed unexpectedly.",
        "logLevel": "CRITICAL",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 1, 1)),
        "processName": "node.exe",
        "processId": "6545",
    },
    {
        "message": "User authenticated successfully.",
        "extra": {"userId": 5},
        "logLevel": "INFO",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 5, 16)),
        "processName": "node.exe",
        "processId": "1337",
    },
    {
        "message": "User could not be found.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "ERROR",
        "applicationName": "Application 2",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 4, 20)),
        "processName": "java.exe",
        "processId": "9385",
    },
]


def test_index_ok(client):
    """ Logger responds to a GET request. """
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


def test_index_rate_limit(client, app):
    """ Logger fails after 5 requests. """
    # Arrange
    # ..enable rate limiting in testing mode
    # app.config["RATELIMIT_ENABLED"] = True

    # Act
    for _ in range(5):
        response = client.get("/")
        assert response.status_code == 200

    response = client.get("/")

    # Assert
    assert response.status_code == 429


@pytest.mark.parametrize("data", sample_logs)
def test_logger_write(client, app, data):
    """ Logger writes to a file. """
    # Arrange
    filename = "log.log"
    message = data["message"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200
    assert filename in os.listdir(app.config["LOG_FOLDER"])
    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        assert message in f.read()


@pytest.mark.parametrize("data", sample_logs)
def test_log_process_name(app, client, data):
    # Arrange
    process_name = data["processName"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert process_name in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_log_process_id(app, client, data):
    # Arrange
    process_id = data["processId"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert process_id in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_log_application_name(app, client, data):
    # Arrange
    application_name = data["applicationName"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert application_name in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_log_level(app, client, data):
    # Arrange
    log_level = data["logLevel"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert log_level in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_log_extra_props(app, client, data):
    # Arrange
    if "extra" not in data:
        pytest.skip()
    extra_props = data["extra"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    # ..order doesn't mattter
    sorted_extra_props = dict()
    for key in sorted(extra_props.keys()):
        sorted_extra_props[key] = extra_props[key]

    assert json.dumps(sorted_extra_props) in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_log_client_time(app, client, data):
    # Arrange
    client_time = data["dateTime"]

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 200

    filename = app.config["LOGGER_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert client_time in last_line


def test_log_write_rate_limit(client, app):
    """ Logger fails after 2 simultaneous requests. """

    # Arrange
    rate_limit = 1
    data = sample_logs[0]

    # ..enable rate limiting in testing mode
    # app.config["RATELIMIT_ENABLED"] = True

    # Act
    for _ in range(rate_limit):
        response = client.post(
            "/logger/log",
            content_type="application/json",
            json=data,
            headers={"x-access-token": data["authToken"]},
        )

        # Assert
        assert response.status_code == 200

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code == 429
