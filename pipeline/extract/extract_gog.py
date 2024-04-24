"""A script which scrapes GOG."""

from os import environ as ENV
import json
from datetime import datetime
from time import sleep

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup


PLATFORM_TITLE = 'window.productcardData.cardProductSystemRequirements'


def get_platforms(game_soup) -> list:
    '''Returns a list of platforms that the game can be run on.'''
    scripts = (game_soup.find_all(
        'script'))

    filtered_script = [
        t.text.strip() for t in scripts if PLATFORM_TITLE in str(t)][0]
    script_dict = [l.split(' = ')
                   for l in filtered_script.split(';')]
    script_dict = [l for l in script_dict if len(l) == 2]
    script_dict = {l[0].strip(): l[1] for l in script_dict}
    return list(json.loads(script_dict[PLATFORM_TITLE]).keys())


def get_soup(web_address: str):
    '''Returns a soup object for a game given the web address.'''
    res = req.get(web_address, timeout=5)
    return BeautifulSoup(res.text, features="html.parser")


def get_detail_links(game_soup) -> list:
    '''Returns a list of detail link class objects for a given
    game soup.'''
    return game_soup.find_all(
        'a', class_='details__link')


def get_json(game_soup) -> dict:
    '''Returns a JSON object about a given game soup.'''
    return json.loads(game_soup.find(
        'script', type='application/ld+json').text)


def get_developer(links: list) -> str:
    '''Returns a string of the developer's name,
    given a game soup.'''
    return [t.text for t in links if 'games?developers=' in t['href']][0]


def get_publisher(links: list) -> str:
    '''Returns a string of the publisher's name,
    given a game soup.'''
    return [t.text for t in links if 'games?publishers=' in t['href']][0]


def get_tags(game_soup) -> list:
    '''Returns a list of tags given a game soup.'''
    tags = game_soup.find_all(
        'span', class_='details__link-text')
    return [t.text for t in tags]


def get_price(game_dict: dict) -> float:
    '''Returns the current price of the game as a float.'''
    return float(game_dict['offers']['price'])


def get_rating(game_dict: dict) -> float:
    '''Returns the average rating for a game as a float,
    out of 5.'''
    if 'aggregateRating' not in game_dict.keys():
        return None
    return float(game_dict['aggregateRating']['ratingValue'])


def get_release_date(game_dict: dict) -> datetime:
    '''Returns a datetime object of the release day.'''
    return datetime.strptime(game_dict['releaseDate'][:-6], '%Y-%m-%dT%H:%M:%S')


def get_platform_ids(platform_str: str) -> list:
    '''Returns a list of platform IDs given a
    string of playable platforms.'''
    id_list = []
    if 'windows' in platform_str:
        id_list.append(1)
    if 'osx' in platform_str:
        id_list.append(2)
    if 'linux' in platform_str:
        id_list.append(3)
    return id_list


def get_title(game_soup_small) -> str:
    '''Returns a string of the game's name.'''
    return game_soup_small.find(
        'div', class_='product-tile__title')['title']


if __name__ == "__main__":

    load_dotenv()

    response_all_games = req.get(ENV["SCRAPING_URL"], timeout=5)
    soup = BeautifulSoup(response_all_games.text, features="html.parser")
    soup = soup.findAll('product-tile', class_='ng-star-inserted')
    for game in soup[:10]:
        address = game.find(
            'a', class_='product-tile product-tile--grid')['href']
        response = req.get(address, timeout=5)
        game_data = BeautifulSoup(response.text, features="html.parser")
        game_json = get_json(game_data)
        link = get_detail_links(game_data)
        print([get_title(game), get_price(game_json), get_developer(link),
               get_publisher(link), get_release_date(game_json),
               get_rating(game_json), 2, get_platform_ids(get_platforms(game_data))])
        sleep(1)
