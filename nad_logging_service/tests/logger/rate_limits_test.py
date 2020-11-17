"""
 * Project Name: NAD-Logging-Service
 * File Name: rate_limits_test.py
 * Programmer: Kai Prince
 * Date: Mon, Nov 16, 2020
 * Description: This file contains rate limit tests for the Logging app.
"""

import os

from .sample_data import good_logs as sample_logs


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


def test_log_write_rate_limit(client, app):
    """ Logger fails after 10 simultaneous requests. """

    # Arrange
    rate_limit = 10
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

    filename = app.config["LOCAL_LOG_FILENAME"]
    assert filename in os.listdir(app.config["LOG_FOLDER"])

    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        last_line = f.readlines()[-1]

    assert "flask-limiter" in last_line
    assert "ratelimit" in last_line
    assert "exceeded" in last_line
