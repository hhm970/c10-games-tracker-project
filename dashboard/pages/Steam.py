'''A script that creates the Steam page for the dashboard.'''

from re import match
from os import environ as ENV, listdir
from datetime import datetime, timedelta

import pandas as pd
import altair as alt
import streamlit as st
from boto3 import client
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


def get_week_list() -> list:
    week_list = []

    for each in range(1, 8):
        day = datetime.now() - timedelta(days=each)
        week_list.append(day.strftime('%Y-%m-%d'))

    return week_list


def metric_games_yest(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""

    yesterday = datetime.now() - timedelta(days=1)
    x = yesterday.strftime('%Y-%m-%d')

    with conn.cursor() as cur:
        cur.execute(f""" SELECT name, rating, price, release_date
                    FROM game 
                    WHERE website_id = 1 AND release_date = '{x}';""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_price(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""

    with conn.cursor() as cur:
        cur.execute(f""" SELECT AVG(price), release_date
                    FROM game 
                    WHERE website_id = 1
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_count(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""

    with conn.cursor() as cur:
        cur.execute(f""" SELECT COUNT(name), release_date
                    FROM game 
                    WHERE website_id = 1
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_rating(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""

    with conn.cursor() as cur:
        cur.execute(f""" SELECT AVG(rating), release_date
                    FROM game 
                    WHERE website_id = 1
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def price_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['AVG price (£)'] = data_df['avg'].apply(lambda x: round(x, 2))
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.X("release_date").sort(sort),
        y="AVG price (£)",
        color="release_date"
    )


def count_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Daily Releases'] = data_df['count']
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.X("release_date").sort(sort),
        y="Daily Releases",
        color="release_date"
    )


def rating_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Average Rating(%)'] = data_df['avg']
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.X("release_date").sort(sort),
        y="Average Rating(%)",
        color="release_date"
    )


if __name__ == "__main__":

    print(get_week_list())

    load_dotenv()
    conn = get_db_connection(ENV)

    metric_df = metric_games_yest(conn)

    no_games = metric_df['name'].nunique()
    avg_rating = metric_df['rating'].mean()
    avg_price = metric_df['price'].mean()

    p_chart = price_chart(metrics_for_graphs_price(conn))
    c_chart = count_chart(metrics_for_graphs_count(conn))
    r_chart = rating_chart(metrics_for_graphs_rating(conn))
    conn.close()

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Steam Summary")
    st.write("---")
    st.subheader(
        "_The latest metrics & graphs!_")

    # metrics
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of new releases yesterday:", no_games)
    with col2:
        st.metric("Average rating of new releases yesterday:",
                  f'{round(avg_rating,2)}%')
    with col3:
        st.metric("Average price of new releases yesterday:",
                  f'£{round(avg_price, 2)}')

    # graphs

    col1, col2 = st.columns(2)
    with col1:

        st.altair_chart(p_chart)
        st.altair_chart(c_chart)
        st.altair_chart(r_chart)

    with col2:
        pass

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
