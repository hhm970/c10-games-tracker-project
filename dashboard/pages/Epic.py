'''A script that creates the epic page for the dashboard.'''

from os import environ as ENV

import streamlit as st


if __name__ == "__main__":
    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("Epic Summary")
    st.write("---")
    st.subheader(
        "_The latest metrics & graphs!_")

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("Home.py")
        st.page_link("pages/Epic.py")
        st.page_link("pages/GOG.py")
        st.page_link("pages/Steam.py")
        st.page_link("pages/Subscribe.py")
