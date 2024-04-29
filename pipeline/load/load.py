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
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.extensions import connection


TAG_EXCEPTIONS = {'Single Player': 'Singleplayer',
                  'Rogue-Lite': 'Roguelite',
                  }


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


def get_game_id_from_inputted_game(inputted_game: list,
                                   cursor: connection.cursor) -> RealDictRow:
    """Given a game that has already been inputted into the database, return its
    matched game_id entry in the database."""
    cursor.execute("""SELECT game_id FROM game
                        WHERE name = %s;""", (inputted_game[0],))

    game_id = cursor.fetchone()['game_id']

    return game_id


def get_dev_id(input_game: list, cursor: connection.cursor) -> RealDictRow:
    """Given a game, returns the corresponding developer_id entry if its developer 
    name is in the developer table, and None otherwise."""

    cursor.execute("""SELECT developer_id FROM developer
                        WHERE developer_name = %s;""", (input_game[3],))

    developer_id_match = cursor.fetchone()

    return developer_id_match


def input_game_dev_get_dev_id(input_game: list, conn: connection) -> int:
    """For each game in our input data, we check if its associated developer is in the
    developer table. If not, we input it into the developer table.
    Returns the developer_id entry from the given developer name."""

    with conn.cursor() as cur:

        developer_id_match = get_dev_id(input_game, cur)

        if developer_id_match is None:

            cur.execute("""INSERT INTO developer (developer_name)
                    VALUES (%s);""", (input_game[3],))

            developer_id_match = get_dev_id(input_game, cur)

    conn.commit()

    return developer_id_match['developer_id']


def get_pub_id(input_game: list, cursor: connection.cursor) -> RealDictRow:
    """Given a game with a publisher entry, returns the corresponding publisher_id entry 
    if its publisher name is in the publisher table, and None otherwise."""

    cursor.execute("""SELECT publisher_id FROM publisher
                        WHERE publisher_name = %s;""", (input_game[4],))

    publisher_id_match = cursor.fetchone()

    return publisher_id_match


def input_game_pub_get_pub_id(input_game: list, conn: connection) -> int:
    """For each game in our input data, we check if its associated publisher is in the
    publisher table. If not, we input it into the publisher table.
    Returns the publisher_id entry from the given publisher name."""

    with conn.cursor() as cur:

        publisher_id_match = get_pub_id(input_game, cur)

        if publisher_id_match is None:

            cur.execute("""INSERT INTO publisher (publisher_name)
                    VALUES (%s);""", (input_game[4],))

            publisher_id_match = get_pub_id(input_game, cur)

    conn.commit()

    return publisher_id_match['publisher_id']


def input_game_into_db(game_data: list[list], conn: connection) -> None:
    """Given our game data, we insert each row into the game table, excluding
    the platforms and tags. We convert developer name and publisher name into
    their respective ids."""

    with conn.cursor() as cur:
        for game in game_data:

            if game[3] is not None:
                game[3] = input_game_dev_get_dev_id(game, conn)
            if game[4] is not None:
                game[4] = input_game_pub_get_pub_id(game, conn)

            cur.execute(
                """INSERT INTO game (name, description, price, developer_id, 
                publisher_id, release_date, rating, website_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", (game[:8]))

    conn.commit()


def input_game_plat_into_db(game_data: list[list], conn: connection) -> None:
    """For each game in our input data, we input all of its supported platforms
    into the platform_assignment table."""

    with conn.cursor() as cur:
        for game in game_data:

            game_id = get_game_id_from_inputted_game(game, cur)

            game_plat_list = game[-1]

            for plat in game_plat_list:
                cur.execute(
                    """INSERT INTO platform_assignment (platform_id, game_id)
                VALUES (%s, %s);""", (plat, game_id))

    conn.commit()


def input_game_tags_into_db(game_data: list[list], conn: connection) -> None:
    """For each game, we iterate through its tags. We use the PostgreSQL extension
    pg_tgm to measure similarity of the tags with existing entries in the tag table,
    appending the tag iterand into the table if no similar entries are detected."""

    with conn.cursor() as cur:
        for game in game_data:

            game_id = get_game_id_from_inputted_game(game, cur)

            game_tags = game[-2]
            if len(game_tags) > 0:

                for tag in game_tags:
                    tag_formatted = tag.title()

                    if tag_formatted in TAG_EXCEPTIONS.keys():
                        tag_formatted = TAG_EXCEPTIONS[tag_formatted]

                    cur.execute("""SELECT tag_id FROM tag
                                WHERE tag_name = %s""",
                                (tag_formatted,))

                    tag_id_match = cur.fetchone()

                    if tag_id_match is None:
                        cur.execute("""INSERT INTO tag (tag_name)
                                    VALUES (%s);""", (tag_formatted,))

                        cur.execute("""SELECT tag_id FROM tag
                                    WHERE tag_name = %s;""", (tag_formatted,))

                        tag_id_match = cur.fetchone()

                    tag_id = tag_id_match['tag_id']

                    cur.execute("""INSERT INTO game_tag_matching (game_id, tag_id)
                                VALUES (%s, %s);""", (game_id, tag_id))

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
