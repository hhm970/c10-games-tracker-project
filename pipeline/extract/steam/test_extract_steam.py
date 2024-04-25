"""Test file for steam_extract.py."""

from steam_extract import (get_rating, get_platform_ids,
get_tags, get_developer, get_publisher, get_name_price_date)


# ratings tests
def test_get_ratings(steam_rating_soup):
    '''Tests the get_ratings function with standard inputs.'''
    assert get_rating(steam_rating_soup) == 50.48


def test_get_ratings_no_reviews(steam_no_rating_soup):
    '''Tests the get_ratings function with no input/reviews.'''
    assert get_rating(steam_no_rating_soup) == 0.00


def test_get_ratings_positive(steam_rating_soup_positive_only):
    '''Tests the get_ratings function with only positive reviews.'''
    assert get_rating(steam_rating_soup_positive_only) == 100.00


def test_get_ratings_negative(steam_rating_soup_negative_only):
    '''Tests the get_ratings function with only negative reviews.'''
    assert get_rating(steam_rating_soup_negative_only) == 0.00


# platform_id tests

def test_get_platform_id_good_input():
    """Test the get_platform function with all good inputs."""
    list_p = ["Windows", "macOS", "Linux"]
    assert get_platform_ids(list_p) == [1, 2, 3]


def test_get_platform_id_bad_input():
    """Test the get_platform function with all good inputs."""
    list_b = ["Widow", "bigmac", "Lemur"]
    assert get_platform_ids(list_b) == []

# get_tags tests


def test_get_tags(steam_tags_good):
    """Test the get_tags function with all good inputs."""
    assert get_tags(steam_tags_good) == ["Horror", "Atmospheric"]


def test_get_tags_no_tags(steam_tags_none):
    """Test the get_tags function with no tags."""
    assert get_tags(steam_tags_none) == []

# get_developer tests


def test_developer(steam_developer_good):
    """Test the get_developer function with a good inputs."""
    assert get_developer(steam_developer_good) == "SCLITIFY IT "


def test_developer_missing(steam_developer_none):
    """Test the get_developer function with a good inputs."""
    assert get_developer(steam_developer_none) is None


# get_publisher tests


def test_publisher(steam_publisher_good):
    """Test the get_developer function with a good inputs."""
    assert get_publisher(steam_publisher_good) == "Inoa Forever"


def test_publisher_missing(steam_developer_none):
    """Test the get_developer function with a no input."""
    assert get_developer(steam_developer_none) is None


# name_price tests

def test_get_name_price_date(search_result):
    """Test the get_name_price_date function is working."""
    assert get_name_price_date(search_result) == [
        'Culling of Normality', 0.0, '24 Apr, 2024']
