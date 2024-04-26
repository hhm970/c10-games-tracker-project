'''A script that sends out SNS alerts when new games come in.'''

from os import environ as ENV

from dotenv import load_dotenv
from boto3 import client

TAG_ARNS = {'Action': 'arn:aws:sns:eu-west-2:129033205317:c10-games-action-tag',
            'Adventure': 'arn:aws:sns:eu-west-2:129033205317:c10-games-adventure-tag',
            'Indie': 'arn:aws:sns:eu-west-2:129033205317:c10-games-indie-tag',
            'Horror': 'arn:aws:sns:eu-west-2:129033205317:c10-games-horror-tag'}


def send_sns(topic: str, games: list, config):
    '''Sends a SNS message to subscribers of a given topic
    about newly released games.'''

    sns = client(
        "sns", aws_access_key_id=config["AWS_KEY"], aws_secret_access_key=config["AWS_SECRET"])
    sns.publish(
        TargetArn=TAG_ARNS[topic],
        Message=f'''Hey there!

Just to let you know there are new games available to play in the {topic} tag.

Here are the games: 

{games}
Speak to you soon,

The GameScraper Team 👾''',
        Subject=f'New games in {topic}!'
    )
    print(f'sent {topic} email')


def format_games_into_list(games: list) -> list:
    '''Takes a list of lists of list and formats this
    for easy manipulation. Returns a list of games with their
    titles, descriptions and tags.'''
    single_list = []
    for list in games:
        single_list += list
    return [[l[0], l[1], l[8]] for l in single_list]


def format_games_into_string(games: list) -> str:
    '''Takes a list of games and turns it into a string which can be used
    in our email.'''
    str_output = ''
    for game in games:
        str_output += game[0] + '\n' + game[1] + '\n\n'
    return str_output


def handler(event=None, context=None):
    '''Sends messages when receives data.'''
    games_unformatted = event
    games_formatted = format_games_into_list(games_unformatted)

    topics = list(TAG_ARNS.keys())
    for topic in topics:
        games_list = [l for l in games_formatted if topic in l[2]]

        if None not in games_list and len(games_list) > 0:
            games_string = format_games_into_string(games_list)
            send_sns(topic, games_string, ENV)


if __name__ == '__main__':
    load_dotenv()

    response = [[
        [
            "Letters & Legends",
            "Embark on an epic linguistic adventure in Letters & Legends, where words, wits, and wisdom are your greatest weapons! Sharpen your tongue and show your enemies who the true wordsmith is!",
            3.99,
            "Bow & Arrow Games",
            "Bow & Arrow Games",
            "2024-04-25 23:00:00",
            'null',
            3,
            [
                "Casual",
                "Puzzle",
                "Cloud Saves",
                "Achievements",
                "Single Player",
                "Controller Support",
                "Indie"
            ],
            [
                1
            ]
        ],
        [
            "Monster Coming",
            "“Monster Coming”is a survivor roguelite game. Dark cracks appear in the sky, and a tide of beasts emerges from them to attack humans. You stand up as one of the braves!",
            2.49,
            "ongmaker",
            "FutureGameStudio,Y.D Studio",
            "2024-04-25 22:00:00",
            'null',
            3,
            [
                "Action",
                "Cloud Saves",
                "Achievements",
                "Single Player",
                "Rogue-Lite",
                "Indie"
            ],
            [
                1
            ]
        ]], [["Wallace & Gromit’s Grand Adventures",
              "Enter the colorful world of West Wallaby Street in a series of four cracking adventures brought to you by Aardman Animations, the creators of the Wallace & Gromit animated films, and award-winning Telltale Games.",
              14.99,
              "Telltale",
              "Telltale",
              "2024-04-25 11:00:00",
              'null',
              3,
              [
                  "Casual",
                  "Single Player",
                  "Adventure",
                  "Telltale Publisher Sale"
              ],
              [
                  1
              ]]], []]
    handler(event=response)
