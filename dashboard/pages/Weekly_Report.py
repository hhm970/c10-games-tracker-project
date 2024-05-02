'''A script that creates a page for our dashboard where you
can subscribe to weekly email reports.'''

from os import environ as ENV

from dotenv import load_dotenv
import streamlit as st
from boto3 import client

from psycopg2 import connect
from psycopg2.extras import RealDictCursor, RealDictRow
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


def verify_email(email_address: str, config):
    '''Checks if an email is already verified,
    if not it is verified.'''
    ses = client(
        "ses", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"], region_name=config['AWS_REGION'])

    if email_address not in ses.list_identities(IdentityType='EmailAddress')["Identities"]:
        res = ses.verify_email_identity(EmailAddress=email_address)
        return res
    return None


def add_to_database(first_name: str, last_name: str, email: str) -> None:
    '''Adds a row to the subscriber table in our database.'''
    if email == '':
        raise ValueError('No email given!')

    conn = get_db_connection(ENV)
    with conn.cursor() as cur:

        cur.execute("""INSERT INTO subscriber (first_name,last_name,email)
                    VALUES (%s,%s,%s)""", (first_name, last_name, email))

    conn.commit()
    conn.close()


def remove_from_database(email: str) -> None:
    '''Removes a subscriber from the subscrber table in our database.'''
    conn = get_db_connection(ENV)
    with conn.cursor() as cur:

        cur.execute("""DELETE FROM subscriber 
                    WHERE email = (%s)""", (email,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    load_dotenv()

    st.title("Weekly Report Emails")
    st.write("---")
    st.subheader(
        "_Get weekly graphs and metrics about the newest games!_")

    with st.form(key='my_form'):
        st.header('Enter your details:')

        first = st.text_input("Enter your first name:")
        last = st.text_input("Enter your last name:")
        email = st.text_input("Enter your email:")
        submit_button = st.form_submit_button(label='Subscribe')

        if submit_button:

            if email == '':
                st.write("No email provided!")
            else:
                try:
                    verify_email(email, ENV)
                    add_to_database(first, last, email)
                    st.write("You have subscribed!")
                    st.write(f"Look out for your weekly report!")
                except:
                    st.write("The email was invalid, try again!")

    st.write("---")
    st.write(
        "In the unlikely event that you would like to stop receiving email notifications:")

    with st.form(key='my_form_2'):
        email = st.text_input("Enter email here:")
        submit_button = st.form_submit_button(label='Unsubscribe')

        if submit_button:
            if email == '':
                st.write("No email provided!")
            else:
                try:
                    verify_email(email, ENV)
                    remove_from_database(email)
                    st.write("You have unsubscribed, we are sorry to see you go.")
                except:
                    st.write("The email was invalid, try again!")

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("Home.py")
        st.page_link("pages/Epic.py")
        st.page_link("pages/GOG.py")
        st.page_link("pages/Steam.py")
        st.page_link("pages/Daily_Notifications.py")
        st.page_link("pages/Weekly_Report.py")
