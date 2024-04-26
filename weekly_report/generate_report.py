import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
import altair as alt
import pandas as pd


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


def num_games_unique_released(conn):
    """Returns the number of unique games released."""
    with conn.cursor() as cur:
        cur.execute("""SELECT count(distinct name)
                    FROM game
                     WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                    AND release_date <= CURRENT_DATE;
                    """)
        num_games = cur.fetchone()['count']
        return num_games


def total_num_games_released(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT count(name)
                    FROM game
                     WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                    AND release_date <= CURRENT_DATE
                    """)
        num_games = cur.fetchone()['count']
        return num_games


def num_games_over_week(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT count(name), release_date
                        FROM game
                        WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND release_date <= CURRENT_DATE GROUP BY release_date;
                        """)
        games = cur.fetchall()
        games = pd.DataFrame(games)
        games['release_date'] = games['release_date'].astype(str)

        chart = alt.Chart(games, title='Number of game releases per day').mark_bar(size=10).encode(
            x='release_date',
            y='count',
        ).properties(
            width=200,
            height=150
        ).configure_mark(
            opacity=0.5,
            color='blue'
        )
        chart.save('chart.png')


def average_price(conn):
    with conn.cursor() as cur:
        cur.execute(
            """SELECT ROUND(AVG(CAST(price AS numeric)), 2)
            AS avg_price FROM game
            WHERE
            release_date >= CURRENT_DATE - INTERVAL '7 days'
            AND release_date <= CURRENT_DATE;""")
        avg_price = cur.fetchone()['avg_price']
        return avg_price


def num_games_per_website(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT w.website_name, count(*) AS num_games FROM game as g LEFT JOIN website AS w ON (g.website_id = w.website_id) WHERE release_date >= CURRENT_DATE - INTERVAL '7 days' AND release_date <= CURRENT_DATE GROUP BY w.website_name;""")
        games = cur.fetchall()
        games = pd.DataFrame(games)
        pie_chart = alt.Chart(games, title='Website-game ratio').mark_arc().encode(
            theta="num_games",
            color=alt.Color('website_name', scale=alt.Scale(scheme='set2'))
        )
        pie_chart.save('pie-chart.png')


def top_five_tags(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON(t.tag_id=gt.tag_id) WHERE gt.game_id IN
                    (SELECT game_id from game WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                     AND release_date <= CURRENT_DATE) GROUP BY t.tag_name ORDER BY count(*) DESC LIMIT 5;
                    """)
        tags = cur.fetchall()
        tag_list = []
        for x in range(len(tags)):
            tag_list.append(tags[x]['tag_name'])
        return tag_list


def tag_game_ratio(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON(t.tag_id=gt.tag_id) WHERE gt.game_id IN
                    (SELECT game_id from game WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                     AND release_date <= CURRENT_DATE) GROUP BY t.tag_name ORDER BY count(*) DESC LIMIT 5;
                    """)
        tags = cur.fetchall()
        tags = pd.DataFrame(tags)
        pie_chart = alt.Chart(tags, title='Tag-game ratio').mark_arc().encode(
            theta="count",
            color=alt.Color('tag_name', scale=alt.Scale(scheme='set2'))
        )
        pie_chart.save('tags_pie-chart.png')


def top_platform(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT p.platform_name, count(*) from platform AS p INNER JOIN platform_assignment AS pa ON(p.platform_id=pa.platform_id) WHERE pa.game_id IN
                    (SELECT game_id from game WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                     AND release_date <= CURRENT_DATE) GROUP BY p.platform_name ORDER BY count(*) DESC LIMIT 1;
                    """)
        platform = cur.fetchone()['platform_name']
        return platform


def average_rating(conn):
    with conn.cursor() as cur:
        cur.execute("""SELECT ROUND(AVG(CAST(rating AS numeric)), 2)
            AS avg_rating
                    FROM game
                     WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                    AND release_date <= CURRENT_DATE;""")
        rating = cur.fetchone()['avg_rating']
        return rating


def generate_pdf(num_unique_games, avg_price, total_games_released, tags, platform, rating):
    pdfmetrics.registerFont(TTFont('jersey_15', 'Jersey15-Regular.ttf'))
    c = canvas.Canvas('Weekly_Report.pdf', pagesize=letter)
    c.setFont('jersey_15', 30)
    c.setFillColorRGB(0.6, 0.09, 10.8)
    c.drawString(100, 750, 'GameScraper Weekly Report')
    c.drawImage('game_scraper_logo.png', x=430, y=735, width=50, height=50)

    c.setFont('jersey_15', 20)
    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 680, 'Number of Games released:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    c.drawString(50, 660, f'{total_games_released}')

    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 640, 'Number of Unique Games released:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    c.drawString(50, 620, f'{num_unique_games}')

    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 600, 'Average Price:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    c.drawString(50, 580, f'£ {avg_price}')

    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 560, 'Top 5 Tags:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    x = 540
    for tag in tags:
        c.drawString(50, x, f'- {tag}')
        x -= 20

    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 420, 'Top Platform:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    c.drawString(50, 400, f'{platform}')

    c.setFillColorRGB(0.6, 0.50, 30.0)
    c.drawString(50, 380, 'Average Rating:')
    c.setFillColorRGB(0.6, 0.70, 35.0)
    c.drawString(50, 360, f'{rating}%')

    c.drawImage('tags_pie-chart.png', x=20, y=155, width=280, height=180)
    c.drawImage('chart.png', x=350, y=450)
    c.drawImage('pie-chart.png', x=320, y=220, width=280, height=180)
    c.showPage()
    c.save()


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection(os.environ)
    total_games_released = total_num_games_released(conn)
    num_unique_games = num_games_unique_released(conn)
    avg_price = average_price(conn)
    num_games_over_week(conn)
    num_games_per_website(conn)
    tags = top_five_tags(conn)
    platform = top_platform(conn)
    rating = average_rating(conn)
    tag_game_ratio(conn)
    generate_pdf(num_unique_games, avg_price,
                 total_games_released, tags, platform, rating)
