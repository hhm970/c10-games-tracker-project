'''A script that creates a notification setup page for our dashboard.'''

from os import environ as ENV

from dotenv import load_dotenv
import streamlit as st
from boto3 import client

TAG_ARNS = {'Action': 'arn:aws:sns:eu-west-2:129033205317:c10-games-action-tag',
            'Adventure': 'arn:aws:sns:eu-west-2:129033205317:c10-games-adventure-tag',
            'Indie': 'arn:aws:sns:eu-west-2:129033205317:c10-games-indie-tag',
            'Horror': 'arn:aws:sns:eu-west-2:129033205317:c10-games-horror-tag'}


def verify_email(email_address: str, config):
    '''Checks if an email is already verified,
    if not it is verified.'''
    ses = client(
        "ses", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"])

    if email_address not in ses.list_identities(IdentityType='EmailAddress')["Identities"]:
        res = ses.verify_email_identity(EmailAddress=email_address)
        return res
    return None


def subscribe_to_topic(email_address: str, config, topic_name: str):
    '''Subscribes a given email to a given topic.'''
    sns = client(
        "sns", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"])

    result = sns.subscribe(
        TopicArn=TAG_ARNS[topic_name],
        Protocol='email',
        Endpoint=email_address,
        ReturnSubscriptionArn=True
    )
    return result


if __name__ == "__main__":
    st.set_page_config(page_title='GameScraper',
                       page_icon=":space_invader:", layout="wide")

    load_dotenv()

    tags = ['Action', 'Adventure', 'Indie', 'Horror']

    st.title("New Release Notifications")
    st.write("---")
    st.subheader(
        "_Get daily updates about new games released in your favourite genres!_")

    with st.form(key='my_form'):
        st.header('Select the topics you want to subscribe to:')

        selected = []
        for tag in tags:
            ticked = st.checkbox(tag)
            if ticked:
                selected.append(tag)
        email = st.text_input("Enter Email:")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            verify_email(email, ENV)
            st.write("You have subscribed!")
            st.write(f"You are now tracking: {', '.join(selected)}")
            for topic in selected:
                subscribe_to_topic(email, ENV, topic)

    with st.sidebar:
        st.title("Navigation Station :rocket:")
        st.write("---")
        st.page_link("http://localhost:8501/",
                     label="Subscribe to Notifications", icon="🔔")
