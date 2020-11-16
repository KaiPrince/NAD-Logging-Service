"""
 * Project Name: NAD-Logging-Service
 * File Name: test_factory.py
 * Programmer: Kai Prince
 * Date: Sun, Nov 15, 2020
 * Description: This file contains tests for the main app.
"""

from nad_logging_service import create_app


def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
