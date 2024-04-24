from os import environ as ENV
from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
from datetime import date
from time import sleep


def get_rating(game_soup: BeautifulSoup) -> float:
    """Function to get the rating percentage of a game from its URL"""

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
    """Function to get the platforms a game is available on from its URL"""

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
            'ul', class_='bb_ul').text for platform in platforms if platform.find('ul', class_='bb_ul')][0]
        if "Windows" in platform_list:
            return "Windows"
        if "mac" in platform_list:
            return "macOS"
        if "Linux" in platform_list:
            return "Linux"
        else:
            return "Windows"


def get_tags(game_soup: BeautifulSoup) -> list:

    return [i.text.strip()
            for i in game_soup.find_all('a', class_='app_tag')]


def get_developer(game_soup: BeautifulSoup) -> str:

    return game_soup.find('div', class_='dev_row').text.split('\n')[-2]


def get_name_price_date(container: BeautifulSoup) -> list:

    title = container.find('span', {'class': 'title'}).text
    price = container.find('div', {'class': "discount_final_price"}).text
    release_date = container.find(
        'div', {'class': "col search_released responsive_secondrow"}).text

    return [title, price, release_date.strip()]


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

    game_res = req.get(game_url)
    game_soup = BeautifulSoup(game_res.text, features="html.parser")

    game_tags = get_tags(game_soup)
    platform_list = get_platforms(game_soup)
    platform_id_list = get_platform_ids(platform_list)
    rating = get_rating(game_soup)
    developer = get_developer(game_soup)
    publisher = 'x'

    return [developer, publisher, date.today(), rating, 1, game_tags, platform_id_list]


def get_everything(soup: BeautifulSoup) -> list:

    final_list = []

    for container in all_containers:

        name_price_date_list = get_name_price_date(container)
        game_url = container['href']
        try:
            detail_list = get_each_game_details(game_url)
            print([name_price_date_list, detail_list])
            final_list.append([name_price_date_list, detail_list])
            sleep(1)
        except IndexError:
            continue

    return final_list


if __name__ == "__main__":

    load_dotenv()

    res = req.get(ENV["BASE_URL"])
    soup = BeautifulSoup(res.text, features="html.parser")

    all_containers = soup.find_all(
        'a', class_="search_result_row")

    print(get_everything(all_containers))
