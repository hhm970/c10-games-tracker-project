"""A script which scrapes GOG."""

from os import environ as ENV
import json
from datetime import datetime

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
from time import sleep


def scrape_from_game_page(web_address: str) -> list:
    '''Returns a list of scraped data.'''
    response = req.get(web_address)
    game_soup = BeautifulSoup(response.text, features="html.parser")

    scripts = (game_soup.find_all(
        'script'))

    filtered_scripts = [
        t for t in scripts if 'window.productcardData.cardProductSystemRequirements' in str(t)][0]
    j = list(json.loads((filtered_scripts).text.split(
        'window.productcardData.cardProductSystemRequirements')[-1][3:].split('window.productcardData.cardProductPromoEndDate')[0].split(';')[0]).keys())
    print(j)

    # game_details = game_soup.find_all(
    #     'div', class_='table__row')
    # platform = game_details[6].find(
    #     'div', class_='details__content table__row-content').text.strip()

    # # print(dev, pub, get_platform_ids(platform), date)


def get_soup(web_address: str):
    '''Returns a soup object for a game given the web address.'''
    response = req.get(web_address)
    return BeautifulSoup(response.text, features="html.parser")


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


def get_price(json: dict) -> float:
    '''Returns the current price of the game as a float.'''
    return float(json['offers']['price'])


def get_rating(json: dict) -> float:
    '''Returns the average rating for a game as a float,
    out of 5.'''
    if 'aggregateRating' not in json.keys():
        return None
    return float(json['aggregateRating']['ratingValue'])


def get_release_date(json: dict) -> datetime:
    '''Returns a datetime object of the release day.'''
    return datetime.strptime(json['releaseDate'][:-6], '%Y-%m-%dT%H:%M:%S')


def get_platform_ids(platform_str: str) -> list:
    '''Returns a list of platform IDs given a
    string of playable platforms.'''
    platform_str = platform_str.lower()
    id_list = []
    if 'windows' in platform_str:
        id_list.append(1)
    if 'mac os' in platform_str:
        id_list.append(2)
    if 'linux' in platform_str:
        id_list.append(3)
    return id_list


if __name__ == "__main__":

    load_dotenv()

    res = req.get(ENV["SCRAPING_URL"])
    soup = BeautifulSoup(res.text, features="html.parser")
    soup = soup.findAll('product-tile', class_='ng-star-inserted')
    for game in soup[9:11]:
        title_object = game.find(
            'div', class_='product-tile__title')['title']
        price = game.find('span', class_='final-value ng-star-inserted')
        price = price.text if price is not None else '£0'
        address = game.find(
            'a', class_='product-tile product-tile--grid')['href']
        website_id = 2
        print(title_object, price, address, website_id)
        scrape_from_game_page(address)
        sleep(1)
