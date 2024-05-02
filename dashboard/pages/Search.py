'''A script that searches the database for games
for the search page on the dashboard.'''

from os import environ as ENV
import streamlit as st
from dotenv import load_dotenv

from psycopg2.extensions import connection
from rapidfuzz.distance import DamerauLevenshtein
from rapidfuzz.process import extractOne
from rapidfuzz.utils import default_process

from pages.functions import (get_db_connection)


def get_name_list(conn: connection) -> list:
    """Returns list of names of all games in the DB."""

    with conn.cursor() as cur:
        cur.execute(""" SELECT name
                    FROM game;""")
        games = cur.fetchall()

    return [row['name'] for row in games]


def show_result(word: str, conn: connection):
    """Returns name of the game found after fuzzy matching."""

    games_list = get_name_list(conn)

    result = extractOne(str(word), games_list, scorer=DamerauLevenshtein.normalized_similarity,
                        score_cutoff=0.8, processor=default_process)

    if result:

        return result[0]
    return "Game not found"


def get_all_game_details(result: str, conn: connection):
    """Returns dictionary containing all the details of the game found."""

    with conn.cursor() as cur:
        cur.execute(f"""SELECT *
                    FROM game as g
                    JOIN developer as d
                    ON g.developer_id = d.developer_id
                    JOIN publisher as p
                    on g.publisher_id = p.publisher_id
                    WHERE name = '{result}';""")
        game = cur.fetchone()
        game_id = game['game_id']

        cur.execute(f"""SELECT t.tag_name
                    FROM tag AS t
                    INNER JOIN game_tag_matching AS gt
                    ON t.tag_id = gt.tag_id
                    JOIN game as g
                    ON g.game_id = gt.game_id
                    WHERE g.game_id = {game_id};""")
        game_tags = cur.fetchall()

        tags = [row['tag_name'] for row in game_tags]

    return {"game_details": game, "game_tags": tags}


if __name__ == "__main__":

    load_dotenv()

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")
    st.divider()
    st.title("Search For A Game:")
    st.divider()

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("Home.py")
        st.page_link("pages/Epic.py")
        st.page_link("pages/GOG.py")
        st.page_link("pages/Steam.py")
        st.page_link("pages/Daily_Notifications.py")
        st.page_link("pages/Weekly_Newsletter.py")
        st.page_link("pages/search.py")

    with st.form("main form", clear_on_submit=True):

        search = st.text_input("Search Game:")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not search:
                st.write("Please Enter A Game To Search")
            else:
                conn_ = get_db_connection(ENV)

                result_ = show_result(search, conn_)
                if result_ != "Game not found":
                    details = get_all_game_details(result_, conn_)

                    conn_.close()
                    st.title("Search Result")
                    st.write("---")
                    st.subheader(f"Game Found: {result_}")
                    st.text(f"Game Title: {details['game_details']['name']}")
                    st.write(
                        f"Description: {details['game_details']['description']}")

                    st.text(f"Price: {details['game_details']['price']}")
                    st.text(
                        f"Developer Name: {details['game_details']['developer_name']}")
                    st.text(
                        f"Publisher Name: {details['game_details']['publisher_name']}")
                    st.text(
                        f"Release Date: {details['game_details']['release_date'].strftime('%d/%m/%Y')}")
                    st.text(
                        "Platforms Available: ")
                    if details['game_details']['website_id'] == 1:
                        st.text(
                            "Steam - https://store.steampowered.com/")
                    elif details['game_details']['website_id'] == 2:
                        st.write("Good Old Games - https://www.gog.com/en/")
                    elif details['game_details']['website_id'] == 3:
                        st.write(
                            "Epic Games - https://store.epicgames.com/en-US/")
                    else:
                        st.text("Missing")
                    st.text("Genre/ Tags:")
                    st.text(f"{details['game_tags']}")
                else:
                    st.text(f"Game not found: {search}")
