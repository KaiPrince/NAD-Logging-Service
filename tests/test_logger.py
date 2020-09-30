# TODO FHC
import os
import pytest


def test_index_ok(client):
    """ Logger responds to a GET request. """
    # Arrange

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


@pytest.mark.parametrize(
    "filename, message",
    [("logfile.log", "This is a test."), ("test.log", "Another test.")],
)
def test_logger_write(client, app, filename, message):
    """ Logger writes to a file. """
    # Arrange
    data = {"filename": filename, "message": message}

    # Act
    response = client.post("/log", content_type="application/json", json=data)

    # Assert
    assert response.status_code == 200
    assert filename in os.listdir(app.config["LOG_FOLDER"])
    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        assert message in f.read()
