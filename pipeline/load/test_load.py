"""Contains unit tests for load.py"""
from datetime import datetime

from unittest.mock import patch, MagicMock

from load import (format_release_date_dt, input_game_into_db,
                  input_game_plat_into_db, input_game_tags_into_db)


def test_format_release_date_dt(test_game_data):
    formatted_game_data = format_release_date_dt(test_game_data)

    m = len(formatted_game_data)

    for i in range(m):
        assert isinstance(formatted_game_data[i][5], datetime) == True


@patch("load.get_db_connection")
def test_input_game_into_db(mock_connection, test_game_data2):

    mock_connection = MagicMock()

    mock_execute = mock_connection.cursor().__enter__().execute

    input_game_into_db(test_game_data2, mock_connection)

    mock_execute.assert_called_once()
