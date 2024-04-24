'''Tests extract_gog.py.'''

from datetime import datetime

from extract_gog import (get_price, get_rating,
                         get_release_date, get_platform_ids)


# get_price

def test_get_price():
    '''Tests the get_price function with standard inputs.'''
    test_json = {'offers': {'price': 72}}
    assert get_price(test_json) == 72


def test_get_price_bad_input():
    '''Tests the get_price function with bad inputs.'''
    test_json = {'offers': 72}
    assert get_price(test_json) == 0


# get_rating

def test_get_rating():
    '''Tests the get_rating function with standard inputs.'''
    test_json = {'aggregateRating': {'ratingValue': 3.5}}
    assert get_rating(test_json) == 3.5


def test_get_rating_no_rating():
    '''Tests the get_rating function with no rating.'''
    test_json = {'somethingElse': 2}
    assert get_rating(test_json) is None


def test_get_rating_bad_input():
    '''Tests the get_rating function with bad inputs.'''
    test_json = {'ratingValue': 2}
    assert get_rating(test_json) is None


# get_release_date

def test_get_release_date():
    '''Tests the get_release_date function with standard inputs.'''
    test_json = {'releaseDate': '2024-04-24T09:55:00+03:00'}
    assert get_release_date(test_json) == datetime(2024, 4, 24, 9, 55)


# get_platform_ids

def test_get_platform_ids():
    '''Tests the get_platform_ids function with standard inputs.'''
    assert get_platform_ids(['windows']) == [1]
    assert get_platform_ids(['osx', 'linux']) == [2, 3]
    assert not get_platform_ids(['wind'])


def test(requests_mock, pytest_fixture):

    requests_mock.
