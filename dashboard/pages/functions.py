"""A file to hold functions used across all pages"""

from os import environ as ENV
from datetime import datetime, timedelta

import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv

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


def get_week_list() -> tuple:
    """Returns a tuple containing the dates 
    of the last seven days (not including today)."""
    w_list = []

    for each in range(1, 8):
        day = datetime.now() - timedelta(days=each)
        w_list.append(day.strftime('%Y-%m-%d'))

    return tuple(w_list)


def filter_tags(data_df: pd.DataFrame, tags_: list, col: str) -> pd.DataFrame:
    """Returns a Data-frame that only has the relevant tags."""
    data_df = data_df[data_df[col].isin(tags_)]

    return data_df


def filter_dates(data_df: pd.DataFrame, dates: list, col: str) -> pd.DataFrame:
    """Returns a Data-frame that only has data from the last 7 days."""
    data_df[col] = data_df[col].astype(str)
    data_df = data_df[data_df[col].isin(dates)]

    return data_df


def metric_games_yest(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of all the games from the yesterday."""

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    with conn_.cursor() as cur:
        cur.execute(f""" SELECT name, rating, price, release_date
                    FROM game
                    WHERE website_id = '{id}' AND release_date = '{yesterday}';""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_price(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of all the average prices for the last week."""
    w_list = get_week_list()

    with conn_.cursor() as cur:
        cur.execute(f""" SELECT AVG(price), release_date
                    FROM game
                    WHERE website_id = '{id}' and release_date in {w_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_count(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of all the number of games for the last week."""
    w_list = get_week_list()

    with conn_.cursor() as cur:
        cur.execute(f""" SELECT COUNT(name), release_date
                    FROM game
                    WHERE website_id = '{id}' and release_date in {w_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_rating(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of all the game ratings for the past week."""
    w_list = get_week_list()

    with conn_.cursor() as cur:
        cur.execute(f""" SELECT AVG(rating), release_date
                    FROM game
                    WHERE website_id = '{id}' and release_date in {w_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_tags(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of all the games tag data from the past week."""
    w_list = get_week_list()

    with conn_.cursor() as cur:
        cur.execute(f"""SELECT t.tag_name, count(*) from tag AS t 
                    INNER JOIN game_tag_matching AS gt 
                    ON t.tag_id = gt.tag_id 
                    WHERE gt.game_id IN
                        (SELECT game_id from game 
                    WHERE website_id = '{id}' 
                    AND release_date 
                    IN {w_list}) 
                    GROUP BY t.tag_name 
                    LIMIT 10;""")
        tag = cur.fetchall()

    return pd.DataFrame(tag)


def metrics_top_ten(conn_: connection, id: int) -> pd.DataFrame:
    """Returns a Data-frame of top rated the games from the last week."""
    w_list = (get_week_list())

    with conn_.cursor() as cur:
        cur.execute(f"""SELECT g.name, g.rating, g.price, d.developer_name, p.publisher_name
    FROM game as g
    JOIN developer as d
    ON g.developer_id = d.developer_id
    JOIN publisher as p
    on g.publisher_id = p.publisher_id
    WHERE g.website_id = '{id}' and g.release_date in {w_list}
    ORDER BY rating DESC LIMIT 10; """)
        tags_ = cur.fetchall()

        min_upper_bd = min(len(tags_) + 1, 11)

    return pd.DataFrame(tags_).set_index(
        pd.Index([str(i) for i in range(1, min_upper_bd)]))


def price_chart(data_df: pd.DataFrame, sorted_=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['AVG price (£)'] = data_df['avg'].apply(lambda x: round(x, 2))
    sort = "-y" if sorted_ else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.Y("AVG price (£)", title='Average Daily Game Price'),
        y=alt.X("release_date").sort(sort),
        color="release_date"
    )


def count_chart(data_df: pd.DataFrame, sorted_=True) -> alt.Chart:
    """"Generates a bar chart of daily number of games releases."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Daily Releases'] = data_df['count']
    sort = "-y" if sorted_ else "x"

    return alt.Chart(data_df).mark_line().encode(
        x=alt.X("release_date",  title='Number Of Daily Releases').sort(sort),
        y=alt.Y("Daily Releases")
    )


def rating_chart(data_df: pd.DataFrame, sorted_=True) -> alt.Chart:
    """""Generates a bar chart of average daily ratings of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Average Rating(%)'] = data_df['avg']
    sort = "-y" if sorted_ else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.Y("Average Rating(%)", title='Average Daily Game Rating'),
        y=alt.X("release_date").sort(sort),
        color="release_date"
    )


def make_tag_chart(data_df: pd.DataFrame, sorted_=True) -> alt.Chart:
    """Generates a bar chart of most popular tags of games in the last week."""

    sort = "-y" if sorted_ else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.X("tag_name").sort(sort),
        y="count",
        color="tag_name"
    )
