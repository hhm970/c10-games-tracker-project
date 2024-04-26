"""
Given some input game data as a list[list] object, we load this data
into our cloud-based database. Each embedded list should have values in the
following order,

name: str; description: str; price: float; developer: str; publisher: str;
release_date: str; rating: int; website_id: int; tags: list[str];
platform: list[int].
"""
from datetime import datetime
from os import environ as ENV

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(config) -> connection:
    """Returns a connection to the database."""

    return connect(
        dbname=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        cursor_factory=RealDictCursor
    )


def format_release_date_dt(game_data: list[list]) -> list[list]:
    """Given our game data, we format the release date as a datetime object."""
    for game in game_data:
        release_date = game[5]
        game[5] = datetime.strptime(release_date, "%Y-%m-%d %H:%M:%S")

    return game_data


def input_game_into_db(game_data: list[list], conn: connection) -> None:
    """Given our game data, we insert each row into the game table, excluding
    the tags and the platforms."""
    with conn.cursor() as cur:
        for game in game_data:
            cur.execute(
                """INSERT INTO game (name, description, price, developer, publisher, 
                release_date, rating, website_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (game[:-2]))

        cur.close()
    conn.commit()


def input_game_dev_into_db(game_data: list[list], conn: connection) -> None:
    """For each game in our input data, we input the values for the developer into the
    developer table."""
    pass


def input_game_pub_into_db(game_data: list[list], conn: connection) -> None:
    """For each game in our input data, we input the values for the publisher into the
    publisher table."""
    pass


def input_game_plat_into_db(game_data: list[list], conn: connection) -> None:
    """For each game in our input data, we input all of its supported platforms
    into the platform_assignment table."""

    with conn.cursor() as cur:
        for game in game_data:
            cur.execute("""SELECT game_id FROM game
                        WHERE name = %s""", (game[0],))

            game_id = cur.fetchone()['game_id']
            game_plat_list = game[-1]

            for plat in game_plat_list:
                cur.execute(
                    """INSERT INTO platform_assignment (platform_id, game_id)
                VALUES (%s, %s)""", (plat, game_id))
        cur.close()
    conn.commit()


def input_game_tags_into_db(game_data: list[list], conn: connection) -> None:
    """For each game, we iterate through its tags. We use the PostgreSQL extension
    pg_tgm to measure similarity of the tags with existing entries in the tag table,
    appending the tag iterand into the table if no similar entries are detected."""

    with conn.cursor() as cur:
        for game in game_data:
            cur.execute("""SELECT game_id FROM game
                        WHERE name = %s""", (game[0],))

            game_id = cur.fetchone()['game_id']
            game_tags = game[-2]
            if len(game_tags) > 0:

                for tag in game_tags:
                    tag_formatted = tag.title()
                    cur.execute("""SELECT tag_id FROM tag
                                WHERE SIMILARITY(%s, tag_name) > 0.8""",
                                (tag_formatted,))
                    tag_id_match = cur.fetchone()

                    if tag_id_match is None:
                        cur.execute("""INSERT INTO tag (tag_name)
                                    VALUES (%s)""", (tag_formatted,))

                        cur.execute("""SELECT tag_id FROM tag
                                    WHERE tag_name = %s""", (tag_formatted,))

                        tag_id_match = cur.fetchone()

                    tag_id = tag_id_match['tag_id']

                    cur.execute("""INSERT INTO game_tag_matching (game_id, tag_id)
                                VALUES (%s, %s)""", (game_id, tag_id))
        cur.close()
    conn.commit()


def handler(event: list[list[list]] = None, context=None) -> None:
    """Takes in an event (ie. the combined game data) and context, and
    loads the game data into the database."""

    conn = get_db_connection(ENV)

    for game_data in event:

        if len(game_data) > 0:

            formatted_game_data = format_release_date_dt(game_data)

            input_game_into_db(formatted_game_data, conn)

            input_game_plat_into_db(formatted_game_data, conn)

            input_game_tags_into_db(formatted_game_data, conn)

    conn.close()
