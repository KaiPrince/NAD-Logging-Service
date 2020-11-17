"""
 * Project Name: NAD-Logging-Service
 * File Name: exception_test.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains exception tests for the Logger app.
"""


import pytest

from .sample_data import exception_logs as sample_logs


@pytest.mark.parametrize("data", sample_logs)
def test_all_bad_tests_fail(client, data):
    """ All these tests should fail """

    # Arrange

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": data["authToken"]},
    )

    # Assert
    assert response.status_code != 200
