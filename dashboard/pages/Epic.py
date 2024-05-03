'''A script that creates the Epic games page for the dashboard.'''

from os import environ as ENV
import streamlit as st
from dotenv import load_dotenv


from pages.functions import (get_db_connection, get_week_list,
                             make_tag_chart, metric_games_yest,
                             metrics_for_graphs_count, metrics_for_graphs_price,
                             metrics_for_graphs_tags, metrics_top_ten_epic, count_chart, price_chart,
                             filter_dates, filter_tags, metric_games_all,
                             metric_games_two_days)


if __name__ == "__main__":

    load_dotenv()
    conn = get_db_connection(ENV)
    week_list = list(get_week_list())

    top_ten_games = metrics_top_ten_epic(conn, 3)
    top_ten_games = top_ten_games.drop('rating', axis=1)
    tag_df = metrics_for_graphs_tags(conn, 3)

    price_df = metrics_for_graphs_price(conn, 3)

    count_df = metrics_for_graphs_count(conn, 3)

    tags = tag_df["tag_name"].to_list()

    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Epic Games Summary")
    st.write("---")
    st.subheader(
        "The latest metrics & graphs!")
    st.text(
        "Brought to you by the GameScraper Team")

    st.divider()
    on = st.toggle("Yesterday")

    if on:
        metric_df = metric_games_yest(conn, 3)
        delta = metric_games_two_days(conn, 3)
        st.write('Metrics For Yesterday:')
    else:
        metric_df = metric_games_all(conn, 3)
        st.write('Metrics For All Data:')

    if not metric_df.empty:
        no_games = metric_df['name'].nunique()

        avg_price = metric_df['price'].mean()
        if on and not delta.empty:
            no_games_delta = delta['name'].nunique()
            avg_price_delta = delta['price'].mean()

        else:
            no_games_delta = 0
            avg_price_delta = 0

    else:
        no_games = 0

        avg_price = 0
        if on:
            no_games_delta = 0
            avg_rating_delta = 0
            avg_price_delta = 0
    conn.close()

    if no_games == 0:
        st.write("No New Games Released Yesterday")

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("Home.py")
        st.page_link("pages/Epic.py")
        st.page_link("pages/GOG.py")
        st.page_link("pages/Steam.py")
        st.page_link("pages/Search.py")
        st.write("---")
        st.page_link("pages/Daily_Notifications.py")
        st.page_link("pages/Weekly_Report.py")
        st.write("---")

        st.title("Filtering")

        creator_options = tags
        filtered_tags = st.multiselect("Available Genres",
                                       options=creator_options,
                                       default=creator_options)
        end_date = st.selectbox(
            'Select Start Date:',
            options=week_list[::-1]
        )

        filtered_days = week_list[:week_list.index(end_date) + 1]

    new_price_df = filter_dates(price_df, filtered_days, "release_date")
    new_count_df = filter_dates(count_df, filtered_days, "release_date")
    new_tag_df = filter_tags(tag_df, filtered_tags, "tag_name")

    c_chart = count_chart(new_count_df, sorted_=False)
    p_chart = price_chart(new_price_df)
    tag_chart = make_tag_chart(new_tag_df)

    if on:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Number of new releases:", no_games,
                      delta=no_games-no_games_delta)
        with col2:
            st.metric("Average price of new releases:",
                      f'£{avg_price:.2f}'.format(avg_price), delta=round(avg_price-avg_price_delta, 2))
        st.subheader("This Weeks Top Ten Games")
        st.write(top_ten_games)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average Price Per Day")
            st.altair_chart(p_chart)
        with col2:
            st.subheader("This Weeks Most Popular Gaming Tags")
            st.altair_chart(tag_chart)

    else:

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Number of new releases:", no_games)
        with col2:
            st.metric("Average price of new releases:",
                      f'£{avg_price:.2f}'.format(avg_price))
        st.subheader("This Weeks Top Ten Games")
        st.write(top_ten_games.rename(
            columns={'name': 'Name', 'price': 'Price', 'developer_name': 'Developer Name', 'publisher_name': 'Publisher', 'rating': 'Rating'}))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Average Price Per Day")
            st.altair_chart(p_chart)
        with col2:
            st.subheader("This Weeks Most Popular Gaming Tags")
            st.altair_chart(tag_chart)
    st.subheader("Daily Releases")
    st.altair_chart(c_chart, use_container_width=True)
