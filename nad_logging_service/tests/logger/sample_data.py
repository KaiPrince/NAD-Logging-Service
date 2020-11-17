"""
 * Project Name: NAD-Logging-Service
 * File Name: _sample_data.py
 * Programmer: Kai Prince
 * Date: Mon, Nov 16, 2020
 * Description: This file contains sample data for testing the logger app.
"""

from datetime import datetime


good_logs = [
    {
        "message": "The app has crashed unexpectedly.",
        "logLevel": "CRITICAL",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime(2020, 1, 1, 8, 54, 30).isoformat(),
        "processName": "node.exe",
        "processId": "6545",
    },
    {
        "message": "User authenticated successfully.",
        "extra": {"userId": 5},
        "logLevel": "INFO",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": "2011-10-05T14:48:00.000Z",
        "processName": "node.exe",
        "processId": "1337",
    },
    {
        "message": "User could not be found.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "ERROR",
        "applicationName": "Application 2",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": "2020-11-15T23:55:51.929Z",
        "processName": "java.exe",
        "processId": "9385",
    },
]

exception_logs = [
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
