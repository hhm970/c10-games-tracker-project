"""This file is responsible for the generating of a pdf summary report and emailing it to users."""
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
import altair as alt
import pandas as pd
import boto3


class StatsRetriever():
    """This class is responsible for the functionality which allows the user
    to retrieve useful stats about the games database."""

    def __init__(self, config=None, website_id: tuple = (1, 2, 3)) -> None:
        """Initialises DB connection and website IDs."""
        self.conn = self.get_db_connection(config)
        self.website_ids = website_id
        self.config = config

    def get_db_connection(self, config) -> connection:
        """Returns a connection to the database."""

        return connect(
            dbname=config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            host=config["DB_HOST"],
            port=config["DB_PORT"],
            cursor_factory=RealDictCursor
        )

    def num_games_unique_released(self):
        """Returns the number of unique games released."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT count(distinct g.name)
                            FROM game AS g
                            WHERE release_date >= CURRENT_DATE - INTERVAL '7 days'
                            AND release_date <= CURRENT_DATE AND g.website_id IN %s;""", (self.website_ids,))

            num_games = cur.fetchone()['count']
            return num_games

    def total_num_games_released(self) -> int:
        """Returns the total number of games released this week (including duplicates)."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT count(name)
                        FROM game AS g
                        WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s
                        """, (self.website_ids,))
            num_games = cur.fetchone()['count']
            return num_games

    def num_games_over_week(self):
        """Returns a chart of the number of games released over the week(per day)."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT count(g.name), g.release_date
                            FROM game AS g
                            WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                            AND g.release_date <= CURRENT_DATE AND g.website_id IN %s GROUP BY g.release_date;
                            """, (self.website_ids,))
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
            if len(self.website_ids) == 3:
                chart.save(f'{self.config["STORAGE_FOLDER"]}/chart_sum.png')
            elif len(self.website_ids) == 2:
                chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/chart_{self.website_ids[0]}_{self.website_ids[1]}.png')
            else:
                chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/chart_{self.website_ids[0]}.png')

    def average_price(self) -> int:
        """Returns the average price of the games from the week."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT ROUND(AVG(CAST(g.price AS numeric)), 2)
                AS avg_price FROM game AS g
                WHERE
                g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                AND g.release_date <= CURRENT_DATE AND g.website_id IN %s;""", (self.website_ids,))
            avg_price = cur.fetchone()['avg_price']
            return avg_price

    def num_games_per_website(self):
        """Returns a pie chart of the number of games released according to website."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT w.website_name, count(*) AS num_games
                         FROM game as g
                         LEFT JOIN website AS w
                        ON (g.website_id = w.website_id)
                         WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                         AND g.release_date <= CURRENT_DATE 
                        AND g.website_id IN %s GROUP BY w.website_name ;""", (self.website_ids,))
            games = cur.fetchall()
            games = pd.DataFrame(games)
            pie_chart = alt.Chart(games, title='Website-game ratio').mark_arc().encode(
                theta="num_games",
                color=alt.Color('website_name', scale=alt.Scale(scheme='set2'))
            )
            if len(self.website_ids) == 3:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/pie_chart_sum.png')
            elif len(self.website_ids) == 2:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/pie_chart_{self.website_ids[0]}_{self.website_ids[1]}.png')
            else:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/pie_chart_{self.website_ids[0]}.png')

    def top_five_tags(self) -> list[str]:
        """Returns the top five tags of this weeks games."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON(t.tag_id=gt.tag_id) WHERE gt.game_id IN
                        (SELECT game_id from game AS g WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s) GROUP BY t.tag_name ORDER BY count(*) DESC LIMIT 5;
                        """, (self.website_ids,))
            tags = cur.fetchall()
            tag_list = []
            for x in range(len(tags)):
                tag_list.append(tags[x]['tag_name'])
            return tag_list

    def tag_game_ratio(self):
        """Returns the proportion of tags in the form of a pie-chart."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON(t.tag_id=gt.tag_id) WHERE gt.game_id IN
                        (SELECT game_id from game AS g WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s) GROUP BY t.tag_name ORDER BY count(*) DESC LIMIT 5;
                        """, (self.website_ids,))
            tags = cur.fetchall()
            tags = pd.DataFrame(tags)
            pie_chart = alt.Chart(tags, title='Tag-game ratio').mark_arc().encode(
                theta="count",
                color=alt.Color('tag_name', scale=alt.Scale(scheme='set2'))
            )
            if len(self.website_ids) == 3:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_sum.png')
            elif len(self.website_ids) == 2:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_{self.website_ids[0]}_{self.website_ids[1]}.png')
            else:
                pie_chart.save(
                    f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_{self.website_ids[0]}.png')

    def top_platform(self) -> str:
        """Returns the top platform name."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT p.platform_name, count(*) from platform AS p
                         INNER JOIN platform_assignment AS pa ON(p.platform_id=pa.platform_id) WHERE pa.game_id IN
                        (SELECT game_id from game AS g WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s)
                        GROUP BY p.platform_name ORDER BY count(*) DESC LIMIT 1;
                        """, (self.website_ids,))
            platform = cur.fetchone()['platform_name']
            return platform

    def average_rating(self) -> float:
        """Returns the average rating of this weeks games."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT ROUND(AVG(CAST(rating AS numeric)), 2)
                AS avg_rating
                        FROM game AS g
                        WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s;""", (self.website_ids,))
            rating = cur.fetchone()['avg_rating']
            return rating

    def top_three_publishers(self) -> list[str]:
        """Returns the top three game publishers of this week."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT p.publisher_name, count(*) AS num_games FROM game as g 
                        LEFT JOIN publisher AS p ON (g.publisher_id = p.publisher_id) 
                        WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s
                        GROUP BY p.publisher_name ORDER BY count(*) DESC LIMIT 3;""", (self.website_ids,))
            publishers = cur.fetchall()
            publisher_list = []
            for x in range(len(publishers)):
                publisher_list.append(publishers[x]['publisher_name'])
            return publisher_list

    def top_three_developers(self) -> list[str]:
        """Returns the top three game developers of this week."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT d.developer_name, count(*) AS num_games FROM game as g
                         LEFT JOIN developer AS d
                         ON (g.developer_id = d.developer_id)
                         WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                         AND g.release_date <= CURRENT_DATE
                        AND g.website_id IN %s
                        GROUP BY d.developer_name ORDER BY count(*) DESC LIMIT 3;""", (self.website_ids,))
            developers = cur.fetchall()
            developer_list = []
            for x in range(len(developers)):
                developer_list.append(developers[x]['developer_name'])
            return developer_list

    def get_website_names(self) -> list[str]:
        """Returns a list of source website used."""
        with self.conn.cursor() as cur:
            cur.execute(
                """SELECT w.website_name FROM website AS w WHERE w.website_id IN %s""", (self.website_ids,))
            websites = cur.fetchall()
            website_list = []
            for x in range(len(websites)):
                website_list.append(websites[x]['website_name'])
            return website_list


class ReportMaker():
    """This class is responsible for the functionality required to generate
      the weekly report."""

    def __init__(self, config) -> None:
        """Initialises configuration to use."""
        self.config = config

    def generate_summary_text(self, canvas_obj, sum):
        """Generates the summary page text for the report."""
        sum.tag_game_ratio()
        sum.num_games_per_website()
        sum.num_games_over_week()

        canvas_obj.setFont('jersey_15', 20)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 680, 'Number of Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(50, 660, f'{sum.total_num_games_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 640, 'Number of Unique Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(50, 620, f'{sum.num_games_unique_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 600, 'Average Price:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(50, 580, f'£ {sum.average_price()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 560, 'Top 5 Tags:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        x = 540
        for tag in sum.top_five_tags():
            canvas_obj.drawString(50, x, f'- {tag}')
            x -= 20

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 420, 'Top Platform:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(50, 400, f'{sum.top_platform()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 380, 'Average Rating:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(50, 360, f'{sum.average_rating()}%')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)

        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_sum.png',
                             x=20, y=155, width=280, height=180)
        canvas_obj.drawString(270, 200, 'Top 3 Developers:')
        x = 180
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        for developer in sum.top_three_developers():
            canvas_obj.drawString(270, x, f'- {developer}')
            x -= 20
        x = 100
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 120, 'Top 3 Publishers:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        for publisher in sum.top_three_publishers():
            canvas_obj.drawString(50, x, f'- {publisher}')
            x -= 20
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(270, 100, 'Sources:')
        x = 80
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        for source in sum.get_website_names():
            canvas_obj.drawString(270, x, f'- {source}')
            x -= 20

        canvas_obj.drawImage(
            f'{self.config["STORAGE_FOLDER"]}/chart_sum.png', x=350, y=450)
        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/pie_chart_sum.png',
                             x=320, y=230, width=280, height=180)
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(300, 20, f'{canvas_obj.getPageNumber()}')

    def individual_summary(self, canvas_obj, website_stats_retriever: StatsRetriever, website_id: int, name: str):
        """Creates individual report text for a website source."""
        website_stats_retriever.tag_game_ratio()
        website_stats_retriever.num_games_over_week()
        canvas_obj.setFont('jersey_15', 30)
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(100, 750, f'GameScraper Weekly Report - {name}')
        canvas_obj.drawImage('game_scraper_logo.png',
                             x=520, y=735, width=50, height=50)

        canvas_obj.setFont('jersey_15', 20)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 680, 'Number of Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(
            50, 660, f'{website_stats_retriever.total_num_games_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 640, 'Average Price:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(
            50, 620, f'£ {website_stats_retriever.average_price()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 580, 'Top 5 Tags:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        x = 560
        for tag in website_stats_retriever.top_five_tags():
            canvas_obj.drawString(50, x, f'- {tag}')
            x -= 20

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 440, 'Top Platform:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(
            50, 420, f'{website_stats_retriever.top_platform()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 380, 'Average Rating:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        canvas_obj.drawString(
            50, 360, f'{website_stats_retriever.average_rating()}')

        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)

        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_{website_id}.png',
                             x=300, y=240, width=280, height=180)
        x = 300
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 320, 'Top 3 Publishers:')
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        for publisher in website_stats_retriever.top_three_publishers():
            canvas_obj.drawString(50, x, f'- {publisher}')
            x -= 20
        canvas_obj.drawImage(
            f'{self.config["STORAGE_FOLDER"]}/chart_{website_id}.png', x=350, y=450)
        x = 160
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 200, 'Top 3 Developers:')
        x = 180
        canvas_obj.setFillColorRGB(0.6, 0.70, 35.0)
        for developer in website_stats_retriever.top_three_developers():
            canvas_obj.drawString(50, x, f'- {developer}')
            x -= 20
        canvas_obj.setFillColorRGB(0.6, 0.70, 30.0)
        canvas_obj.drawString(300, 20, f'{canvas_obj.getPageNumber()}')

    def generate_report(self):
        sum = StatsRetriever(self.config)
        steam = StatsRetriever(self.config, (1,))
        gog = StatsRetriever(self.config, (2,))
        epic = StatsRetriever(self.config, (3,))
        pdfmetrics.registerFont(TTFont('jersey_15', 'Jersey15-Regular.ttf'))
        c = canvas.Canvas(
            f'{self.config["STORAGE_FOLDER"]}/Weekly_Report.pdf', pagesize=letter)
        c.setFont('jersey_15', 30)
        c.setFillColorRGB(0.6, 0.09, 10.8)
        c.drawString(100, 750, 'GameScraper Weekly Report')
        c.drawImage('game_scraper_logo.png',
                    x=430, y=735, width=50, height=50)
        self.generate_summary_text(c, sum)
        c.showPage()
        # Individual reports
        # Steam
        self.individual_summary(c, steam, 1, "Steam")
        c.showPage()
        # GOG
        self.individual_summary(c, gog, 2, "GOG")
        c.showPage()
        # EPIC
        self.individual_summary(c, epic, 3, "Epic")
        c.save()


class Alerter():
    """This class is responsible for the functionality 
    required to email the report out."""

    def __init__(self, config) -> None:
        """Initialises configuration and database connection."""
        self.config = config
        self.db_conn = self.connect_db()

    def connect_db(self):
        """Returns database connection object."""
        return connect(
            dbname=self.config["DB_NAME"],
            user=self.config["DB_USER"],
            password=self.config["DB_PASSWORD"],
            host=self.config["DB_HOST"],
            port=self.config["DB_PORT"],
            cursor_factory=RealDictCursor
        )

    def get_subscription_emails(self) -> list[str]:
        """Returns a list of subscriber emails from the database."""
        with self.db_conn.cursor() as cur:
            cur.execute("""SELECT email FROM subscriber;""")
            subscribers = cur.fetchall()
            subscriber_list = []
            for x in range(len(subscribers)):
                subscriber_list.append(subscribers[x]['email'])
            return subscriber_list

    def send_email(self, subscriber_list: list[str]):
        """Sends Email containing weekly report to subscribers."""

        client = boto3.client("ses",
                              region_name="eu-west-2",
                              aws_access_key_id=self.config["ACCESS_KEY_ID"],
                              aws_secret_access_key=self.config["SECRET_ACCESS_KEY"])
        message = MIMEMultipart()
        message["Subject"] = "GameScraper Weekly Report"

        attachment = MIMEApplication(
            open(f'{self.config["STORAGE_FOLDER"]}/Weekly_Report.pdf', 'rb').read())
        attachment.add_header('Content-Disposition',
                              'attachment', filename='report.pdf')
        message_text = MIMEText('Hi -- here is the weekly GameScraper report!')
        message.attach(message_text)
        message.attach(attachment)

        client.send_raw_email(
            Source='trainee.setinder.manic@sigmalabs.co.uk',
            Destinations=subscriber_list,
            RawMessage={
                'Data': message.as_string()
            }
        )


if __name__ == "__main__":
    load_dotenv()
    r = ReportMaker(os.environ)
    r.generate_report()
    a = Alerter(os.environ)
    subscribers = a.get_subscription_emails()
    a.send_email(subscribers)
