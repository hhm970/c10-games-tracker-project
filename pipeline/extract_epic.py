"""Extracting game details from EPIC games"""

from os import environ
from datetime import datetime,timedelta

from dotenv import load_dotenv
import requests as req


def get_games_data(config) -> list[dict] :
    """Returns games json data."""
    today_date = str(datetime.now().date())
    yesterday_date = str((datetime.now()-timedelta(days=1.0)).date())
    query = """{{
	Catalog {{
		searchStore (count:40, sortBy: "releaseDate", sortDir: "DESC",
								 releaseDate: "[{previous_day},{today}]") {{
			elements {{
				title,
				releaseDate,
				description,
				publisherDisplayName,
				developerDisplayName
				currentPrice
				seller {{
					name
				}}
				tags {{
					name
					groupName
				}}
				categories {{
					path
				}}
			}}
		}}
	}}
}}""".format(previous_day = yesterday_date,today = today_date)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"
    }
    res = req.post(config["BASE_URL"], json={"query": query}, headers=headers,timeout=10)
    game_data = res.json()
    games = game_data['data']['Catalog']['searchStore']['elements']
    return games


def get_game_title(game_obj:dict) -> str:
    """Returns title from game json object."""
    return game_obj['title']

def get_game_description(game_obj:dict) -> str:
    """Returns game description from game json object."""
    return game_obj['description']


def get_tags(game_obj:dict)->list[str]:
    """Returns tag ids from game json object."""
    game_tags = []
    tags = game_obj['tags']
    for tag in tags:
        game_tags.append(tag['name'])
    return game_tags


def get_developer(game_obj:dict) -> str :
    """Returns developer from game json object."""
    return game_obj['developerDisplayName']


def get_publisher(game_obj:dict) -> str:
    """Returns publisher from game json object."""
    return game_obj['publisherDisplayName']


def get_price(game_obj:dict) -> float:
    """Returns price from game json object."""
    return game_obj['currentPrice']/100


def get_release_date(game_obj:dict):
    """Returns release date from game json object."""
    return datetime.fromisoformat(game_obj['releaseDate'][0:-5])


def get_platform_ids(game_tags:list[str]) -> list[int]:
    """Returns platform ids from game json object."""
    platform_ids = []
    if 'Windows' in game_tags:
        platform_ids.append(1)
    if 'Mac OS' in game_tags:
        platform_ids.append(2)
    return platform_ids


def get_game_details(game_obj:dict) -> list:
    """Returns list of relevant details from game json object."""
    title = get_game_title(game_obj)
    description = get_game_description(game_obj)
    tags = get_tags(game_obj)
    developer = get_developer(game_obj)
    publisher = get_publisher(game_obj)
    price = get_price(game_obj)
    release_date = get_release_date(game_obj)
    platform_ids = get_platform_ids(tags)
    return [title,description ,price, developer, publisher,
            release_date, None, 3, tags, platform_ids]


def get_all_games_details(games_obj:dict) -> list:
    """Returns list of games and their relevant details."""
    games_details = []
    for game in games_obj:
        games_details.append(get_game_details(game))
    return games_details


if __name__ == "__main__":
    load_dotenv()
    games = get_games_data(environ)
    if len(games):
        games_details = get_all_games_details(games)