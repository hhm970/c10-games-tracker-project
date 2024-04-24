"""Script to scrape relevant data from the epic games website."""

from os import environ as ENV
from datetime import datetime, date
from time import sleep
from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup


def get_rating(game_soup: BeautifulSoup) -> float:
    """Function to get the rating percentage of a game from its URL."""

    rating = game_soup.find('div', class_="review_ctn")
    if "There are no reviews for this product" in rating:
        return 0.00
    else:
        positive = rating.find('label', {'for': "review_type_positive"})
        negative = rating.find('label', {'for': "review_type_negative"})
        if positive:
            p_num = int(positive.find(
                'span', class_='user_reviews_count').text.strip('()'))

        else:
            return 0.00
        if negative:
            n_num = int(negative.find(
                'span', class_='user_reviews_count').text.strip('()'))
        else:
            return 100

        return round((p_num/(p_num+n_num)) * 100, 2)


def get_platforms(game_soup: BeautifulSoup) -> list:
    """Function to get the platforms a game is available on from its URL."""

    if game_soup.findAll(
            'div', class_="sysreq_tab"):
        platforms = [i.text.strip() for i in game_soup.findAll(
            'div', class_="sysreq_tab")]
        for i in range(len(platforms)):
            if "Linux" in platforms[i]:
                platforms[i] = "Linux"
        return platforms
    else:
        platforms = game_soup.findAll(
            'div', class_="sysreq_contents")
        platform_list = [platform.find(
            'ul', class_='bb_ul').text for platform in platforms if platform.find(
                'ul', class_='bb_ul')][0]
        if "Windows" in platform_list:
            return ["Windows"]
        if "mac" in platform_list:
            return ["macOS"]
        if "Linux" in platform_list:
            return ["Linux"]

        return ["Windows"]


def get_tags(game_soup: BeautifulSoup) -> list:
    """Function to get the tags of a game from its URL."""
    return [i.text.strip()
            for i in game_soup.find_all('a', class_='app_tag')]


def get_developer(game_soup: BeautifulSoup) -> str:
    """Function to get the developing company of a game from its URL."""
    return game_soup.find('div', class_='dev_row').text.split('\n')[-2]


def get_publisher(game_soup: BeautifulSoup) -> str:
    """Function to get the publisher of a game from its URL."""
    pub = game_soup.find_all('div', class_='dev_row')
    pub_list = [x.text.split('\n') for x in pub]
    for each in pub_list:
        if 'Publisher:' in each:
            return each[-2]
    return None


def get_name_price_date(container: BeautifulSoup) -> list:
    """Function that returns a list containing the:
      title, price and date of a game from its from the search page."""
    title = container.find('span', {'class': 'title'}).text
    price = container.find('div', {'class': "discount_final_price"}).text
    if price == "Free":
        float_price = 0.00
    else:
        float_price = float(price[1:])
    release_date = container.find(
        'div', {'class': "col search_released responsive_secondrow"}).text

    return [title, float_price, release_date.strip()]


def get_description(game_soup: BeautifulSoup) -> str:
    """Function to get the description of a game from its URL."""
    return game_soup.find('div', id='game_area_description').text.strip()


def get_platform_ids(platform: list) -> list:
    '''Returns a list of platform IDs given a
    string of playable platforms.'''
    id_list = []
    if 'Windows' in platform:
        id_list.append(1)
    if 'macOS' in platform:
        id_list.append(2)
    if 'Linux' in platform:
        id_list.append(3)
    return id_list


def get_each_game_details(game_url: str) -> list:
    """Function to get all the details of a game from its URL
    returns a list."""
    game_res = req.get(game_url, timeout=10)
    game_soup = BeautifulSoup(game_res.text, features="html.parser")

    game_tags = get_tags(game_soup)
    platform_list = get_platforms(game_soup)
    platform_id_list = get_platform_ids(platform_list)
    rating = get_rating(game_soup)
    developer = get_developer(game_soup)
    publisher = get_publisher(game_soup)
    description = get_description(game_soup)

    return [description, developer, publisher, date.today(), rating, 1, game_tags, platform_id_list]


def get_everything(all_web_containers: BeautifulSoup) -> list[list]:
    """Function to combine all the details of from the search results page
      returns a list of lists"""

    final_list = []

    for container in all_web_containers:

        name_price_date_list = get_name_price_date(container)
        game_date = datetime.strptime(
            name_price_date_list[-1], "%d %b, %Y").date()
        name_price_date_list.pop(-1)
        if game_date != date.today():
            continue
        game_url = container['href']
        try:
            detail_list = get_each_game_details(game_url)
            description = detail_list.pop(0)
            name_price_date_list.append(name_price_date_list[1])
            name_price_date_list[1] = description
            final_list.append(name_price_date_list + detail_list)
            sleep(1)
        except IndexError:
            continue

    return final_list


if __name__ == "__main__":

    load_dotenv()

    res = req.get(ENV["BASE_URL"], timeout=10)
    soup = BeautifulSoup(res.text, features="html.parser")

    all_containers = soup.find_all(
        'a', class_="search_result_row")

    print(get_everything(all_containers))
