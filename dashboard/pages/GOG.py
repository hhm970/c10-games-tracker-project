'''A script that creates the GOG page for the dashboard.'''

from os import environ as ENV

import streamlit as st


if __name__ == "__main__":
    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    st.title("GOG Summary")
    st.write("---")
    st.subheader(
        "_The latest metrics & graphs!_")

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
