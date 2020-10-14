# TODO FHC
import os
import pytest
from datetime import datetime

sample_logs = [
    {
        "message": "The app has crashed unexpectedly.",
        "logLevel": "CRITICAL",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime(2020, 1, 1),
    },
    {
        "message": "User authenticated successfully.",
        "extra": {"userId": 5},
        "logLevel": "INFO",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime(2020, 5, 16),
    },
    {
        "message": "User could not be found.",
        "extra": {"userId": 5, "endpoint": "/users/5"},
        "logLevel": "ERROR",
        "applicationName": "BingoBangoBongo",
        "authToken": "eyy35t4m5vtk489k7vtk5ivk8ct74",
        "dateTime": datetime(2020, 4, 20),
    },
]


def test_index_ok(client):
    """ Logger responds to a GET request. """
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "message",
    ["first test.", "This is a test.", "Another test."],
)
def test_logger_write(client, app, message):
    """ Logger writes to a file. """
    # Arrange
    filename = "log.log"
    data = {"message": message}

    # Act
    response = client.post(
        "/logger/log",
        content_type="application/json",
        json=data,
        headers={"x-access-token": "abc"},
    )

    # Assert
    assert response.status_code == 200
    assert filename in os.listdir(app.config["LOG_FOLDER"])
    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        assert message in f.read()


@pytest.mark.skip("TODO")
def test_auth_token_with_payload():
    pass
