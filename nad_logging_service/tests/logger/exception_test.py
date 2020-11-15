"""
 * Project Name: NAD-Logging-Service
 * File Name: exception_test.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains exception tests for the Logger app.
"""


import os
import pytest
from datetime import datetime
import json

sample_logs = [
    {
        "message": "This datetime is malformed.",
        "logLevel": "CRITICAL",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 1, 1))[5:],
        "processName": "node.exe",
        "processId": "6545",
    },
    {
        "message": "This log entry is massive.",
        "extra": {"userId": 5, "massive": "i" * 500},
        "logLevel": "INFO",
        "applicationName": "BingoBangoBongo" + "i" * 500,
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 5, 16)),
        "processName": "node.exe" + "i" * 500,
        "processId": "1337" + "i" * 500,
    },
    {
        "message": "This log level is invalid.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "thisleveldoesnotexist",
        "applicationName": "Application 2",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 4, 20)),
        "processName": "java.exe",
        "processId": "9385",
    },
    {
        "message": "The extra data is malformed.",
        "extra": '{"userId" 5 "endpo}',
        "logLevel": "CRITICAL",
        "applicationName": "Application 2",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 4, 20)),
        "processName": "java.exe",
        "processId": "9385",
    },
    {
        "message": "The auth token is invalid.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "CRITICAL",
        "applicationName": "Application 2",
        "authToken": "thisauthtokenisbad",
        "dateTime": str(datetime(2020, 4, 20)),
        "processName": "java.exe",
        "processId": "9385",
    },
    {
        "message": "The processId is not an integer.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "CRITICAL",
        "applicationName": "Application 2",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": str(datetime(2020, 4, 20)),
        "processName": "java.exe",
        "processId": "thisisabadprocessid",
    },
]


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
