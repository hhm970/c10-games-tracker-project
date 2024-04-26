'''Tests extract_gog.py.'''

from datetime import datetime

from pytest import raises

from extract_gog import (get_price, get_rating, get_developer,
                         get_release_date, get_platform_ids, get_publisher,
                         get_tags, get_title, get_description)


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
    assert get_rating(test_json) == 70


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


# get_publisher

def test_get_publisher_extract_correct_publisher(gog_fake_links):
    '''Tests get_publisher on a standard input.'''
    assert get_publisher(gog_fake_links) == 'publisher1'


def test_get_publisher_extract_bad_input(gog_fake_links_bad):
    '''Tests get_publisher on a bad input.'''
    assert get_publisher(gog_fake_links_bad) is None


# get_developer

def test_get_developer_extract_correct_developer(gog_fake_links):
    '''Tests get_developer on a standard input.'''
    assert get_developer(gog_fake_links) == 'dev'


def test_get_developer_extract_bad_input(gog_fake_links_bad):
    '''Tests get_developer on a bad input.'''
    assert get_developer(gog_fake_links_bad) is None


# get_tags

def test_get_tags_good_input(gog_tags):
    '''Tests get_tags on a standard input.'''
    assert get_tags(gog_tags) == ['tag7', 'tag72']


def test_get_tags_bad_input(gog_tags_bad):
    '''Tests get_tags on a bad input.'''
    assert get_tags(gog_tags_bad) == []


# get_title

def test_get_title_good_input(gog_title):
    '''Tests get_title on a standard input.'''
    assert get_title(gog_title) == 'goodtitle'


def test_get_title_bad_input(gog_tags_bad):
    '''Tests get_title on a bad input.'''
    with raises(TypeError):
        get_title(gog_tags_bad)


# get_title

def test_get_description_good_input(gog_description):
    '''Tests get_description on a standard input.'''
    assert get_description(
        gog_description) == 'a very nice really thorough description'
