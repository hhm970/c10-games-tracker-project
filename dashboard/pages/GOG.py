'''A script that creates the GOG page for the dashboard.'''

from os import environ as ENV
import streamlit as st
from dotenv import load_dotenv


from pages.functions import (get_db_connection, get_week_list,
                             make_tag_chart, metric_games_yest,
                             metrics_for_graphs_count, metrics_for_graphs_price,
                             metrics_for_graphs_rating, metrics_for_graphs_tags,
                             metrics_top_ten, rating_chart, count_chart, price_chart,
                             filter_dates, filter_tags)


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection(ENV)
    week_list = list(get_week_list())

    metric_df = metric_games_yest(conn, 2)
    top_ten_games = metrics_top_ten(conn, 2)
    tag_df = metrics_for_graphs_tags(conn, 2)
    tags = tag_df["tag_name"].to_list()

    if not metric_df.empty:
        no_games = metric_df['name'].nunique()
        avg_rating = metric_df['rating'].mean()
        avg_price = metric_df['price'].mean()
    else:
        no_games = 0
        avg_rating = 0
        avg_price = 0

    price_df = metrics_for_graphs_price(conn, 2)
    count_df = metrics_for_graphs_count(conn, 2)
    rating_df = metrics_for_graphs_rating(conn, 2)

    conn.close()

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Good Old Games (GOG) Summary")
    st.write("---")
    st.subheader(
        "The latest metrics & graphs!")
    st.text(
        "Brought to you by the GameScraper Team")

    st.divider()
    if no_games == 0:
        st.write("No New Games Released Yesterday")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Number of new releases yesterday:", no_games)
    with col2:
        st.metric("Average rating of new releases yesterday:",
                  f'{round(avg_rating,2)}%')
    with col3:
        st.metric("Average price of new releases yesterday:",
                  f'£{avg_price:.2f}'.format(avg_price))

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("Home.py")
        st.page_link("pages/Epic.py")
        st.page_link("pages/GOG.py")
        st.page_link("pages/Steam.py")
        st.page_link("pages/Daily_Notifications.py")
        st.page_link("pages/Weekly_Newsletter.py")
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
    c_chart = count_chart(new_count_df, sorted_=False)
    r_chart = rating_chart(new_rating_df)

    st.subheader("This Weeks Top Ten Games")
    st.write(top_ten_games)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average Price Per Day")
        st.altair_chart(p_chart)
        st.subheader("Average Rating Per Day")
        st.altair_chart(r_chart)

    with col2:
        st.subheader("This Weeks Most Popular Gaming Tags")
        st.altair_chart(tag_chart)

    st.subheader("Daily Releases")
    st.altair_chart(c_chart, use_container_width=True)
