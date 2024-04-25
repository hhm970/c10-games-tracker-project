"""Contains unit tests for load.py"""
from datetime import datetime

import pytest

from load import (format_release_date_dt, input_game_into_db,
                  input_game_plat_into_db, input_game_tags_into_db)


def test_format_release_date_dt(test_game_data):
    formatted_game_data = format_release_date_dt(test_game_data)
    assert isinstance(formatted_game_data[0][5], datetime) == True
