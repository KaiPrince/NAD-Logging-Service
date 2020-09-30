# TODO FHC
import pytest


def test_index_ok(client):
    """ Logger responds to a GET request. """
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


def test_logger_echo(client):
    """ Logger echos a POST request. """
    # Arrange
    data = {"key": "value"}

    # Act
    response = client.post("/log", content_type="application/json", json=data)

    # Assert
    assert response.status_code == 200
    assert response.json == data
