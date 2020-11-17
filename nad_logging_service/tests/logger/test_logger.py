"""
 * Project Name: NAD-Logging-Service
 * File Name: test_logger.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains tests for the logger app.
"""

import json
import os
from datetime import datetime

import pytest
from dateutil.parser import isoparse

from .sample_data import good_logs as sample_logs


def test_index_ok(client):
    """ Logger responds to a GET request. """
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


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
    client_time = isoparse(data["dateTime"])
    formatted_client_time = client_time.strftime("%Y-%m-%d %H:%M:%S %Z")

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

    assert formatted_client_time in last_line


@pytest.mark.parametrize("data", sample_logs)
def test_logger_timezone_utc(client, app, data):
    """ DateTimes must always be stored in UTC/GMT. """

    # Arrange

    # ..clients are responsible for sending UTC time.
    # client_local_time = data["dateTime"]
    # client_utc_time = datetime(client_local_time)

    server_local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    server_utc_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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

        assert server_utc_time in last_line
        if server_utc_time != server_local_time:
            assert server_local_time not in last_line
        # assert client_utc_time in log_line and client_local_time not in log_line
