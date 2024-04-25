"""This file contains tests for the extract_epic.py functions."""
import datetime

from pipeline.extract.epic.extract_epic import get_games_data, get_game_details, epic_extract_process


def test_pull_data_from_graphql(requests_mock, epic_game_post_response):
    """Tests successful post request."""

    config = {
        'BASE_URL': 'http://www.epic/test/graphql.com'
    }
    requests_mock.post('http://www.epic/test/graphql.com',
                       json=epic_game_post_response)
    result = get_games_data(config)

    assert result == epic_game_post_response['data']['Catalog']['searchStore']['elements']


def test_correct_game_details_pulled(epic_game_data_game_obj):
    """Tests successful extracting of data from json object."""
    result = get_game_details(epic_game_data_game_obj)
    print(result)
    assert result == ['Vengeance of Mr. Peppermint',
                      "Long ago, they killed his sister. Now, he will kill them.",
                      19.99, 'Hack The Publisher', 'Freedom Games', datetime.datetime(
                          2024, 4, 24, 16, 0), None, 3,
                      ['Action', 'Action-Adventure', 'Single Player',
                       'Indie'], [1, 2]]


def test_no_new_games(requests_mock, epic_empty_post_request):
    """Tests error handling of grabbing data."""
    config = {
        'BASE_URL': 'http://www.epic/test/graphql.com'
    }
    requests_mock.post('http://www.epic/test/graphql.com',
                       json=epic_empty_post_request)
    result = epic_extract_process(config)
    assert result == []


def test_no_one_new_games(requests_mock, epic_game_post_response):
    """Tests error handling of grabbing data."""
    config = {
        'BASE_URL': 'http://www.epic/test/graphql.com'
    }
    requests_mock.post('http://www.epic/test/graphql.com',
                       json=epic_game_post_response)
    result = epic_extract_process(config)
    assert result == [['Vengeance of Mr. Peppermint',
                       "Long ago, they killed his sister. Now, he will kill them.",
                      19.99, 'Hack The Publisher', 'Freedom Games', datetime.datetime(
                          2024, 4, 24, 16, 0),
                       None, 3, ['Action', 'Action-Adventure',
                                 'Single Player', 'Indie'], [1, 2]]]
