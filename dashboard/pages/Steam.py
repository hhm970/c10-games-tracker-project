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


def price_chart(data_df: pd.DataFrame) -> alt.Chart:
    """Returns a bar chart of average temperature or soil moisture per plant."""

    data_df['release_date'] = data_df['release_date'].astype(str)

    sort = "-x" if sorted else "y"

    return alt.Chart(data_df).mark_bar().encode(
        x="date",
        y="price"
    )


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection(ENV)

    metric_df = metric_games_yest(conn)

    no_games = metric_df['name'].nunique()
    avg_rating = metric_df['rating'].mean()
    avg_price = metric_df['price'].mean()

    p_chart = price_chart(metric_df, 'price', True)

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Steam Summary")
    st.write("---")
    st.subheader(
        "_The latest metrics & graphs!_")

    # metrics

    st.metric("Number of new releases yesterday:", no_games)
    st.metric("Average rating of new releases yesterday:",
              f'{round(avg_rating,2)}%')
    st.metric("Average price of new releases yesterday:",
              f'£{round(avg_price, 2)}')

    # graphs

    st.altair_chart(p_chart)

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
