"""Script to scrape relevant data from the epic games website."""

from os import mkdir, environ as ENV
from datetime import datetime, date, timedelta
from time import sleep

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver


def get_rating(game_soup: BeautifulSoup) -> float:
    """Function to get the rating percentage of a game from its URL."""

    rating = game_soup.find('div', class_="review_ctn")
    if "There are no reviews for this product" in rating:
        return None
    else:
        positive = rating.find('label', {'for': "review_type_positive"})
        negative = rating.find('label', {'for': "review_type_negative"})
        if positive:
            p_num = int(positive.find(
                'span', class_='user_reviews_count').text.strip('()').replace(',', ''))
        else:
            return 0.00

        if negative:
            n_num = int(negative.find(
                'span', class_='user_reviews_count').text.strip('()').replace(',', ''))
        else:
            return 100

        return round((p_num/(p_num+n_num)) * 100, 2)


def get_single_platform(game_soup: BeautifulSoup) -> list:
    """Function to get the platforms a game is available on from its URL."""
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
        return get_single_platform(game_soup)


def get_tags(game_soup: BeautifulSoup) -> list:
    """Function to get the tags of a game from its URL."""
    return [i.text.strip()
            for i in game_soup.find_all('a', class_='app_tag')]


def get_developer(game_soup: BeautifulSoup) -> str:
    """Function to get the developing company of a game from its URL."""
    if game_soup.find('div', class_='dev_row'):
        return game_soup.find('div', class_='dev_row').text.split('\n')[-2]
    return None


def get_publisher(game_soup: BeautifulSoup) -> str:
    """Function to get the publisher of a game from its URL."""
    pub = game_soup.find_all('div', class_='dev_row')
    pub_list = [x.text.split('\n') for x in pub]
    for each in pub_list:
        if 'Publisher:' in each:
            return each[-2].strip()
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
    platform_id_translations = {'Windows': 1, 'macOS': 2, 'Linux': 3}
    for tag in platform:
        platform_id = platform_id_translations.get(tag, None)
        if platform_id is not None:
            id_list.append(platform_id)
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

    return [description, developer, publisher, rating, 1, game_tags, platform_id_list]


def grab_all_games_details(all_web_containers: BeautifulSoup) -> list[list]:
    """Function to combine all the details of from the search results page
      returns a list of lists."""

    final_list = []

    for container in all_web_containers:

        name_price_date_list = get_name_price_date(container)
        game_date = datetime.strptime(
            name_price_date_list[-1], "%d %b, %Y").date()
        name_price_date_list.pop(-1)
        if game_date < (datetime.today() - timedelta(days=7)).date():
            break
        n_game_date = datetime.combine(game_date, datetime.min.time())
        game_url = container['href']

        detail_list = get_each_game_details(game_url)
        description = detail_list.pop(0)
        name_price_date_list.append(name_price_date_list[1])
        name_price_date_list[1] = description
        detail_list.insert(2, n_game_date)
        final_list.append(name_price_date_list + detail_list)
        sleep(0.5)

    return final_list


def handler(event: dict = None, context=None) -> list[list]:
    """Collects the required data for each game and then returns a
    list of lists of this data."""

    cookies = {"name": "timezoneOffset", "value": "3600,0"
               }

    browser = webdriver.Firefox()
    browser.get(ENV["STEAM_BASE_URL"])
    browser.set_page_load_timeout(10)
    browser.add_cookie(cookies)

    for i in range(9):
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(0.5)

    content = browser.execute_script("return document.body.innerHTML;")
    soup = BeautifulSoup(content, features="html.parser")
    browser.quit()
    all_containers = soup.find_all(
        'a', class_="search_result_row")
    return grab_all_games_details(all_containers)


if __name__ == "__main__":
    load_dotenv()
    print(handler())
