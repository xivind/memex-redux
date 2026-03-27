# tests/conftest.py
import pytest
from unittest.mock import patch


@pytest.fixture
def no_db():
    """Prevent real DB calls during server tests."""
    with patch("core.db_connection.check_db_connection", return_value=False):
        yield
