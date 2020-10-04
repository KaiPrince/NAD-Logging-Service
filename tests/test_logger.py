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
    "message",
    ["This is a test.", "Another test."],
)
def test_logger_write(client, app, message):
    """ Logger writes to a file. """
    # Arrange
    filename = "log.log"
    data = {"message": message}

    # Act
    response = client.post("/log", content_type="application/json", json=data)

    # Assert
    assert response.status_code == 200
    assert filename in os.listdir(app.config["LOG_FOLDER"])
    with open(os.path.join(app.config["LOG_FOLDER"], filename)) as f:
        assert message in f.read()


"""
body: JSON.stringify({
        message: 'message',
        logLevel: '1',
        applicationId: '0x01',
        authToken: 'asdfsagtgrtg',
        dateTime: new Date('2020-01-01'),
      })
"""


# def test_logger_parse_options():
#     """ """
#     pass
