"""A script which scrapes GOG."""

from os import environ as ENV
import json
from datetime import datetime, timedelta
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


def get_description(game_soup) -> str:
    '''Returns a string description about the game.'''
    description_soup = game_soup.find(
        'div', class_='description')
    return description_soup.text.strip()


def get_game_details(game) -> list:
    '''Returns a list of key data points about a given
    game soup.'''

    address = game.find(
        'a', class_='product-tile product-tile--grid')['href']
    response = req.get(address, timeout=5)
    game_data = BeautifulSoup(response.text, features="html.parser")
    game_json = get_json(game_data)
    release_date = get_release_date(game_json)

    link = get_detail_links(game_data)
    return [get_title(game), get_description(game_data), get_price(game_json),
            get_developer(link), get_publisher(link), release_date,
            get_rating(game_json), 2, get_tags(game_data),
            get_platform_ids(get_platforms(game_data))]


def get_games_from_page(soup) -> list:
    '''Searches all games released recently, and
    returns a list of lists containing details about
    all the games released in the last 24 hours.'''
    yesterday = datetime.now() - timedelta(days=1)
    recently_released = []
    for game in soup:
        game_data = get_game_details(game)
        release_date = game_data[5]
        if release_date > yesterday:
            recently_released.append(game_data)
            sleep(1)
        else:
            break
    return recently_released


def search_pages_last_day() -> list:
    '''Searches all pages until the last game on the
    page was released more than a day ago.Returns a
    list of lists of games released less than 24 hours
    ago.'''
    load_dotenv()
    counter = 1
    games_from_page = req.get(
        f'{ENV["SCRAPING_URL"]}&page={counter}', timeout=5)
    page_soup = BeautifulSoup(games_from_page.text, features="html.parser")
    games_soup = page_soup.findAll('product-tile', class_='ng-star-inserted')
    game_data_list = get_games_from_page(games_soup)
    more_pages = True
    while more_pages:
        sleep(1)
        counter += 1
        games_from_page = req.get(
            f'{ENV["SCRAPING_URL"]}&page={counter}', timeout=5)
        page_soup = BeautifulSoup(games_from_page.text, features="html.parser")
        games_soup = page_soup.findAll(
            'product-tile', class_='ng-star-inserted')
        game_data = get_games_from_page(games_soup)
        if len(game_data) == 0:
            more_pages = False
        else:
            game_data_list = game_data_list.append(game_data)

    return game_data_list


if __name__ == "__main__":
    new_games = search_pages_last_day()
