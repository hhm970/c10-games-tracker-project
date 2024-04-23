"""Extracting game details from EPIC games"""

from os import environ
from dotenv import load_dotenv

import requests as req


def get_games_data(config):
    """Returns games json data."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
    }
    res = req.get(config["BASE_URL"], headers=headers, timeout=10)
    game_data = res.json()
    games = game_data['data']['Catalog']['searchStore']['elements']
    return games


def get_game_title(game_obj):
    """Returns title from game json object."""
    return game_obj['title']


def get_tags(game_obj):
    """Returns tag ids from game json object."""
    return game_obj['tags']


def get_developer(game_obj):
    """Returns developer from game json object."""
    return game_obj['developerDisplayName']


def get_publisher(game_obj):
    """Returns publisher from game json object."""
    return game_obj['publisherDisplayName']


def get_price(game_obj):
    """Returns price from game json object."""
    return game_obj['currentPrice']/100


def get_release_date(game_obj):
    """Returns release date from game json object."""
    return game_obj['releaseDate']


def get_platform_ids(game_tags):
    """Returns platform ids from game json object."""
    platform_ids = []
    if any(tag['id'] == '9547' for tag in game_tags):
        platform_ids.append(1)
    if any(tag['id'] == '10719' for tag in game_tags):
        platform_ids.append(2)
    return platform_ids


def get_game_details(game_obj):
    """Returns list of relevant details from game json object."""
    title = get_game_title(game_obj)
    tags = get_tags(game_obj)
    developer = get_developer(game_obj)
    publisher = get_publisher(game_obj)
    price = get_price(game_obj)
    release_date = get_release_date(game_obj)
    platform_ids = get_platform_ids(tags)
    return [title, price, developer, publisher, release_date, None, 3, tags, platform_ids]


def get_all_games_details(games_obj):
    """Returns list of games and their relevant details."""
    games_details = []
    for game in games_obj:
        games_details.append(get_game_details(game))
    return games_details


if __name__ == "__main__":
    load_dotenv()
    games = get_games_data(environ)
    games_details = get_all_games_details(games)
