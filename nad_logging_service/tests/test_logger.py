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
    ["This is a test.", "Another test."],
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


@pytest.mark.parametrize("application_name", ["BingoBangoBongo", "application_2"])
def test_register_application(client, app, application_name):
    """The register service route consumes an application name
    and produces a token."""

    # Arrange

    # Act
    response = client.post(
        "/registry/register",
        content_type="application/json",
        json={"app_name": application_name},
    )

    # Assert
    assert response.status_code == 201

    assert "token" in response.json

    applications = client.get("/registry/").json["applications"]
    assert application_name in applications


@pytest.mark.parametrize(
    "app_name, token",
    [("app_1", "freagtkgthsgsdhfjkaf"), ("app_2", "123456ytghbj876ir5")],
)
def test_get_auth_token(client, app, mocker, app_name, token):
    # Arrange
    mock_registry = {app_name: token}
    mocker.patch("nad_logging_service.auth.app_registry", mock_registry)

    # Act
    response = client.post(
        "/auth/token", content_type="application/json", json={"app_name": app_name}
    )

    # Assert
    assert response.status_code == 200

    assert "token" in response.json

    response_token = response.json["token"]
    assert response_token == token


@pytest.mark.parametrize("app_name", [("app_1"), ("app_2")])
def test_register_and_auth(client, app, app_name):
    """ Register an application, and verify the token is valid. """

    # Arrange

    # Act
    response = client.post(
        "/registry/register",
        content_type="application/json",
        json={"app_name": app_name},
    )

    # Assert
    assert response.status_code == 201
    assert "token" in response.json

    # Act
    token = response.json["token"]

    auth_response = client.post(
        "/auth/verify_token",
        content_type="application/json",
        json={"app_name": app_name, "token": token},
    )

    # Assert
    assert auth_response.status_code == 200
