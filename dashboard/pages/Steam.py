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

    return tuple(week_list)


def filter_tags(data_df: pd.DataFrame, tags: list, col: str) -> pd.DataFrame:

    data_df = data_df[data_df[col].isin(tags)]

    return data_df


def filter_dates(data_df: pd.DataFrame, dates: list, col: str) -> pd.DataFrame:

    data_df[col] = data_df[col].astype(str)
    data_df = data_df[data_df[col].isin(dates)]

    return data_df


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
    week_list = get_week_list()

    with conn.cursor() as cur:
        cur.execute(f""" SELECT AVG(price), release_date
                    FROM game
                    WHERE website_id = 1 and release_date in {week_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_count(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""
    week_list = get_week_list()

    with conn.cursor() as cur:
        cur.execute(f""" SELECT COUNT(name), release_date
                    FROM game
                    WHERE website_id = 1 and release_date in {week_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_rating(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""
    week_list = get_week_list()

    with conn.cursor() as cur:
        cur.execute(f""" SELECT AVG(rating), release_date
                    FROM game
                    WHERE website_id = 1 and release_date in {week_list}
                    GROUP BY release_date;""")
        steam_games = cur.fetchall()

    return pd.DataFrame(steam_games)


def metrics_for_graphs_tags(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""
    week_list = (get_week_list())

    with conn.cursor() as cur:
        cur.execute(f"""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON t.tag_id = gt.tag_id WHERE gt.game_id IN
                    (SELECT game_id from game WHERE website_id = 1 AND release_date IN {week_list}) GROUP BY t.tag_name LIMIT 10;""")
        tags = cur.fetchall()

    return pd.DataFrame(tags)


def metrics_top_ten(conn: connection) -> pd.DataFrame:
    """Returns a dataframe of all the games tag data from the steam website in the database"""
    week_list = (get_week_list())

    with conn.cursor() as cur:
        cur.execute(f"""SELECT g.name, g.rating, g.price, d.developer_name, p.publisher_name
                    FROM game as g
                    JOIN developer as d
                    ON g.developer_id = d.developer_id
                    JOIN publisher as p
                    on g.publisher_id = p.publisher_id
                    WHERE g.website_id = 1 and g.release_date in {week_list}
                    ORDER BY rating DESC LIMIT 10;""")
        tags = cur.fetchall()

    return pd.DataFrame(tags)


def price_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['AVG price (£)'] = data_df['avg'].apply(lambda x: round(x, 2))
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.Y("AVG price (£)", title='Average Daily Game Price'),
        y=alt.X("release_date").sort(sort),
        color="release_date"
    )


def count_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Daily Releases'] = data_df['count']
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_line().encode(
        x=alt.X("release_date",  title='Number Of Daily Releases').sort(sort),
        y=alt.Y("Daily Releases")
    )


def rating_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    data_df['release_date'] = data_df['release_date'].astype(str)
    data_df['Average Rating(%)'] = data_df['avg']
    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.Y("Average Rating(%)", title='Average Daily Game Rating'),
        y=alt.X("release_date").sort(sort),
        color="release_date"
    )


def make_tag_chart(data_df: pd.DataFrame, sorted=True) -> alt.Chart:
    """"Generates a bar chart of average daily prices of games over their release dates."""

    sort = "-y" if sorted else "x"

    return alt.Chart(data_df).mark_bar().encode(
        x=alt.X("tag_name").sort(sort),
        y="count",
        color="tag_name"
    )


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection(ENV)
    week_list = list(get_week_list())

    metric_df = metric_games_yest(conn)
    top_ten_games = metrics_top_ten(conn)
    tag_df = metrics_for_graphs_tags(conn)
    tags = tag_df["tag_name"].to_list()

    no_games = metric_df['name'].nunique()
    avg_rating = metric_df['rating'].mean()
    avg_price = metric_df['price'].mean()

    price_df = metrics_for_graphs_price(conn)
    count_df = metrics_for_graphs_count(conn)
    rating_df = metrics_for_graphs_rating(conn)

    conn.close()

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Steam Summary")
    st.write("---")
    st.subheader(
        "_The latest metrics & graphs!_")
    st.text(
        "Brought to you by the GameScraper Team")

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

    # sidebar
    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.title("Filtering")

        creator_options = tags
        filtered_tags = st.multiselect("Available Genres",
                                       options=creator_options,
                                       default=creator_options)

        end_date = st.select_slider(
            'Select a range of dates',
            options=week_list
        )

    filtered_days = week_list[:week_list.index(end_date) + 1]

    new_price_df = filter_dates(price_df, filtered_days, "release_date")
    new_count_df = filter_dates(count_df, filtered_days, "release_date")
    new_rating_df = filter_dates(rating_df, filtered_days, "release_date")
    new_tag_df = filter_tags(tag_df, filtered_tags, "tag_name")

    tag_chart = make_tag_chart(new_tag_df)
    p_chart = price_chart(new_price_df)
    c_chart = count_chart(new_count_df)
    r_chart = rating_chart(new_rating_df)

    # graphs

    st.subheader("This Weeks Top Ten Games")
    st.write(top_ten_games)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average Price Per Day")
        st.altair_chart(p_chart)
        st.subheader("Average Rating Per Day")
        st.altair_chart(r_chart)

    with col2:
        st.subheader("Most Popular Gaming Tags")
        st.altair_chart(tag_chart)

    st.subheader("Daily Releases")
    st.altair_chart(c_chart, use_container_width=True)
