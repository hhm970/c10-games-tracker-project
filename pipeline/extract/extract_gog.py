"""A script which scrapes GOG."""

from os import environ as ENV

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
from time import sleep


def scrape_from_game_page(web_address: str) -> list:
    '''Returns a list of scraped data.'''
    response = req.get(web_address)
    game_soup = BeautifulSoup(response.text, features="html.parser")
    tags = game_soup.find_all(
        'span', class_='details__link-text')
    tags = [t.text for t in tags]
    dev = game_soup.find_all(
        'div', class_='details__content table__row-content')
    dev = game_soup.find_all('a', class_='details__link')[-3].text
    pub = game_soup.find_all('a', class_='details__link')[-2].text
    date = game_soup.find_all(
        'div', class_='details__content table__row-content')
    print(date)
    '''<div class="details__content table__row-content"><span ng-cloak="">{{'2024-04-19T00:00:00+03:00' | date: 'longDate' : ' +0300 ' }}</span></div>,'''

    print(dev, pub)


if __name__ == "__main__":

    load_dotenv()

    res = req.get(ENV["SCRAPING_URL"])
    soup = BeautifulSoup(res.text, features="html.parser")
    soup = soup.findAll('product-tile', class_='ng-star-inserted')
    for game in soup[:1]:
        title_object = game.find(
            'div', class_='product-tile__title')['title']
        price = game.find('span', class_='final-value ng-star-inserted')
        price = price.text if price is not None else '$0'
        address = game.find(
            'a', class_='product-tile product-tile--grid')['href']
        print(title_object, price, address)
        scrape_from_game_page(address)
        sleep(1)
