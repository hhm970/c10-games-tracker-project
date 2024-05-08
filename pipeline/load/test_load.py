"""Contains unit tests for load.py"""
from datetime import datetime

from unittest.mock import patch, MagicMock
from psycopg2.extras import execute_values, RealDictCursor, RealDictRow
from psycopg2.extensions import connection

from load import (format_release_date_dt, input_game_dev_get_dev_id,
                  input_game_pub_get_pub_id, input_game_into_db)


def test_format_release_date_dt(test_game_data):
    """Asserts that the function format_release_date_dt()
    formats every timestamp string into a datetime object."""
    formatted_game_data = format_release_date_dt(test_game_data)

    m = len(formatted_game_data)

    for i in range(m):
        assert isinstance(formatted_game_data[i][5], datetime) == True


@patch("load.get_db_connection")
def test_input_game_dev_get_dev_id(mock_connection, test_game_data):
    """Asserts that the database is accessed upon inputting game data
    into input_game_dev_get_dev_id()."""

    mock_connection = MagicMock()

    mock_cursor = mock_connection.cursor()

    mock_execute = mock_cursor.__enter__().execute

    for game in test_game_data:

        input_game_dev_get_dev_id(game, mock_connection)

        mock_execute.assert_called()


@patch("load.get_db_connection")
def test_input_game_pub_get_pub_id(mock_connection, test_game_data):
    """Asserts that the database is accessed upon inputting game data
    into input_game_pub_get_pub_id()."""

    mock_connection = MagicMock()

    mock_cursor = mock_connection.cursor()

    mock_execute = mock_cursor.__enter__().execute

    for game in test_game_data:

        input_game_pub_get_pub_id(game, mock_connection)

        mock_execute.assert_called()
