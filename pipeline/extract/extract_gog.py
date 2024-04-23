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

    details_links = game_soup.find_all(
        'a', class_='details__link')
    dev = [t.text for t in details_links if 'games?developers=' in t['href']]
    # print(dev)
    dev = game_soup.find_all('a', class_='details__link')[-3].text
    pub = game_soup.find_all('a', class_='details__link')[-2].text

    game_json = json.loads(game_soup.find(
        'script', type='application/ld+json').text)

    print(get_release_date(game_json))

    game_details = game_soup.find_all(
        'div', class_='table__row')
    platform = game_details[6].find(
        'div', class_='details__content table__row-content').text.strip()

    # print(dev, pub, get_platform_ids(platform), date)


def get_tags(soup) -> list:
    '''Returns a list of tags given a game soup.'''
    tags = soup.find_all(
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
    return datetime.strptime(json['releaseDate'], )


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
    for game in soup[:10]:
        title_object = game.find(
            'div', class_='product-tile__title')['title']
        price = game.find('span', class_='final-value ng-star-inserted')
        price = price.text if price is not None else '£0'
        address = game.find(
            'a', class_='product-tile product-tile--grid')['href']
        website_id = 2
        # print(title_object, price, address, website_id)
        scrape_from_game_page(address)
        sleep(1)
