"""Given our games data in a lists of lists format, we load this data 
into our cloud-based database."""
from os import environ as ENV
from dotenv import load_dotenv

from boto3 import client
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


if __name__ == "__main__":

    load_dotenv()

    conn = get_db_connection(ENV)
