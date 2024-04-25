"""Given some input game data as a list[list] object, we load this data 
into our cloud-based database. Each embedded list should have values in the 
following order,

name: str; description: str; price: float; developer: str; publisher: str; 
release_date: datetime; rating: float; website_id: int; tags: list[str]; 
platform: list[int]. 
"""
from os import environ as ENV
from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extras import RealDictCursor, execute_values
from psycopg2.extensions import connection


def get_db_connection(config) -> connection:
    """Returns a connection to the database."""

    return connect(
        dbname=config["DB_NAME"],
        user=config.get("DB_USER"),
        password=config.get("DB_PASSWORD"),
        host=config.get("DB_HOST"),
        port=config.get("DB_PORT", 5432),
        cursor_factory=RealDictCursor
    )


def input_game_into_db(game_data: list[list], conn: connection) -> None:
    """Given our game data, we insert each row into the game table, excluding
    the tags and the platforms."""
    with conn.cursor() as cur:
        for game in game_data:
            cur.execute(
                """INSERT INTO game (name, description, price, developer, publisher, 
                release_date, rating, website_id)
                VALUES %s""", game[:-2])

        cur.close()
    conn.commit()


def input_game_plat_into_db(game_data: list[list], conn: connection) -> None:
    """For each game in our input data, we input all of its supported platforms
    into the platform_assignment table."""
    with conn.cursor() as cur:
        for game in game_data:
            cur.execute("""SELECT game_id FROM game
                        WHERE name = %s""", (game_data[0],))

            game_id = cur.fetchone()[0]
            game_plat_list = game[-1]

            for plat in game_plat_list:
                cur.execute(
                    """INSERT INTO platform_assignment (platform_id, game_id)
                    VALUES %s""", (plat, game_id))
        cur.close()
    conn.commit()


def input_game_tags_into_db(game_data: list[list], conn: connection) -> None:
    """"""
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection(ENV)
