"""This file is responsible for the generating of a pdf summary report and emailing it to users."""
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import *
from reportlab.lib import styles
from reportlab.platypus import Frame, Paragraph
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from wordcloud import WordCloud
import altair as alt
import pandas as pd
import boto3
from dotenv import load_dotenv


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
                            AND release_date <= CURRENT_DATE 
                        AND g.website_id IN %s;""", (self.website_ids,))

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

            chart = alt.Chart(games, title='Number of game releases per day').mark_bar(size=30).encode(
                x=alt.X('release_date', title='Date'),
                y=alt.Y('count', title='Count'),
            ).properties(
                width=800,
                height=200
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
            ).properties(
                width=200,
                height=200
            ).configure_legend(
                titleFontSize=10,
                labelFontSize=10
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

    def get_tags_word_count(self):
        """Returns the result of a sql query which returns tags and the
          number of times it occurs in set of website ids.."""
        with self.conn.cursor() as cur:
            cur.execute("""SELECT t.tag_name, count(*) from tag AS t INNER JOIN game_tag_matching AS gt ON(t.tag_id=gt.tag_id) WHERE gt.game_id IN
                        (SELECT game_id from game AS g WHERE g.release_date >= CURRENT_DATE - INTERVAL '7 days'
                        AND g.release_date <= CURRENT_DATE AND g.website_id IN %s) GROUP BY t.tag_name ORDER BY count(*) DESC;
                        """, (self.website_ids,))
            tags_word_count = cur.fetchall()
            return tags_word_count

    def get_word_cloud(self):
        """Creates a word cloud based on the tags of each website."""
        tags_word_count = self.get_tags_word_count()
        tag_list = [tags_word_count[x]['tag_name']
                    for x in range(len(tags_word_count))]
        word_counts = [tags_word_count[x]['count']
                       for x in range(len(tags_word_count))]

        res = {tag_list[i]: word_counts[i] for i in range(len(tag_list))}

        fog_machine = WordCloud(
            background_color='#FFFFFF', colormap="viridis")
        fog_machine.generate_from_frequencies(res)
        fog_machine.to_image()

        # saving image to file
        if len(self.website_ids) == 3:
            fog_machine.to_file(
                f'{self.config["STORAGE_FOLDER"]}/tags_sum_wordcloud.png')
        elif len(self.website_ids) == 2:
            fog_machine.to_file(
                f'{self.config["STORAGE_FOLDER"]}/tags_wordcloud_{self.website_ids[0]}_{self.website_ids[1]}.png')
        else:
            fog_machine.to_file(
                f'{self.config["STORAGE_FOLDER"]}/tags_wordcloud_{self.website_ids[0]}.png')


class ReportMaker():
    """This class is responsible for the functionality required to generate
      the weekly report."""

    def __init__(self, config) -> None:
        """Initialises configuration to use."""
        self.config = config
        self.page_width = 595
        self.page_length = 842

    def generate_summary_text(self, canvas_obj, sum):
        """Generates the summary page text for the report."""
        sum.num_games_per_website()
        sum.num_games_over_week()
        sum.get_word_cloud()
        canvas_obj.setFont('jersey_15', 20)
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 670, 'Number of Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 650, f'{sum.total_num_games_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(300, 670, 'Number of Unique Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(300, 650, f'{sum.num_games_unique_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 620, 'Average Price:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 600, f'£ {sum.average_price()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(210, 620, 'Average Rating:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(225, 600, f'{sum.average_rating()}%')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(400, 620, 'Top Platform:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(400, 600, f'{sum.top_platform()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)

        # Create a custom style
        custom_style = styles.getSampleStyleSheet(
        )['Normal']  # Start with a default style
        custom_style.fontName = 'jersey_15'
        custom_style.fontSize = 20
        custom_style.textColor = (0.6, 0.50, 30.0)
        custom_style.alignment = 0
        custom_style.leading = 17

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 335, 'Top 3 Developers:')
        frame = Frame(50, 270, 250, 70, showBoundary=0)
        developer_list = sum.top_three_developers()
        for x in range(len(developer_list)):
            if developer_list[x] is None:
                developer_list[x] = "None"
        frame.addFromList([Paragraph(f"- {string}\n", custom_style)
                           for string in developer_list], canvas_obj)

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(330, 335, 'Top 3 Publishers:')
        frame = Frame(330, 270, 240, 70, showBoundary=0)
        publisher_list = sum.top_three_publishers()
        for x in range(len(publisher_list)):
            if publisher_list[x] is None:
                publisher_list[x] = "None"
        frame.addFromList([Paragraph(f"- {string}\n", custom_style)
                           for string in publisher_list], canvas_obj)

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 220, ' Top Tags:')

        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/tags_sum_wordcloud.png',
                             x=45, y=70, width=210, height=135)
        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/pie_chart_sum.png',
                             x=295, y=45, width=280, height=200)

        canvas_obj.drawImage(
            f'{self.config["STORAGE_FOLDER"]}/chart_sum.png', x=75, y=370, width=450, height=200)

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString((self.page_width/2.0), 20,
                              f'{canvas_obj.getPageNumber()}')

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0, 0.15)
        canvas_obj.roundRect(25, 585, 550, 125, 4, stroke=1, fill=1)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(25, 370, 550, 200, 4, stroke=1, fill=0)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0, 0.15)
        canvas_obj.roundRect(25, 260, 550, 95, 4, stroke=1, fill=1)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(25, 45, 250, 200, 4, stroke=1, fill=0)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(290, 45, 285, 200, 4, stroke=1, fill=0)
        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8, 0.5)

    def individual_summary(self, canvas_obj, website_stats_retriever: StatsRetriever, website_id: int, name: str):
        """Creates individual report text for a website source."""
        website_stats_retriever.tag_game_ratio()
        website_stats_retriever.num_games_per_website()
        website_stats_retriever.num_games_over_week()
        website_stats_retriever.get_word_cloud()

        canvas_obj.setFont('jersey_15', 20)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(50, 715, f'Date: {str(datetime.now().date())}')
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 695, f'Summary - {name}')
        canvas_obj.setFont('jersey_15', 30)
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        text_width = pdfmetrics.stringWidth(
            'GameScraper Weekly Report', 'jersey_15', 30)
        canvas_obj.drawString((self.page_width-text_width) /
                              2.0, 750, 'GameScraper Weekly Report')
        canvas_obj.drawImage('game_scraper_logo.png',
                             x=470, y=735, width=50, height=50)
        canvas_obj.setFont('jersey_15', 20)
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 670, 'Number of Games released:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(
            50, 650, f'{website_stats_retriever.total_num_games_released()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 620, 'Average Price:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(
            50, 600, f'£ {website_stats_retriever.average_price()}')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(210, 620, 'Average Rating:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(
            225, 600, f'{website_stats_retriever.average_rating()}%')

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(400, 620, 'Top Platform:')
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0)
        canvas_obj.drawString(
            400, 600, f'{website_stats_retriever.top_platform()}')

        # Create a custom style
        custom_style = styles.getSampleStyleSheet(
        )['Normal']  # Start with a default style
        custom_style.fontName = 'jersey_15'
        custom_style.fontSize = 20
        custom_style.textColor = (0.6, 0.50, 30.0)
        custom_style.alignment = 0
        custom_style.leading = 17

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 335, 'Top 3 Developers:')
        frame = Frame(50, 270, 250, 70, showBoundary=0)
        developer_list = website_stats_retriever.top_three_developers()
        for x in range(len(developer_list)):
            if developer_list[x] is None:
                developer_list[x] = "None"
        frame.addFromList([Paragraph(f"- {string}\n", custom_style)
                           for string in developer_list], canvas_obj)
        x = 310

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(330, 335, 'Top 3 Publishers:')
        frame = Frame(330, 270, 240, 70, showBoundary=0)
        publisher_list = website_stats_retriever.top_three_publishers()
        for x in range(len(publisher_list)):
            if publisher_list[x] is None:
                publisher_list[x] = "None"
        frame.addFromList([Paragraph(f"- {string}\n", custom_style)
                           for string in publisher_list], canvas_obj)
#
        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString(50, 220, ' Top Tags:')

        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/tags_wordcloud_{website_id}.png',
                             x=45, y=70, width=210, height=135)
        canvas_obj.drawImage(f'{self.config["STORAGE_FOLDER"]}/tags_pie_chart_{website_id}.png',
                             x=320, y=50, width=250, height=200)

        canvas_obj.drawImage(
            f'{self.config["STORAGE_FOLDER"]}/chart_{website_id}.png',  x=75, y=370, width=450, height=200)

        canvas_obj.setFillColorRGB(0.6, 0.09, 10.8)
        canvas_obj.drawString((self.page_width/2.0), 20,
                              f'{canvas_obj.getPageNumber()}')

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0, 0.15)
        canvas_obj.roundRect(25, 585, 550, 125, 4, stroke=1, fill=1)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(25, 370, 550, 200, 4, stroke=1, fill=0)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.setFillColorRGB(0.6, 0.50, 30.0, 0.15)
        canvas_obj.roundRect(25, 260, 550, 95, 4, stroke=1, fill=1)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(25, 45, 250, 200, 4, stroke=1, fill=0)

        canvas_obj.setStrokeColorRGB(0.6, 0.09, 10.8)
        canvas_obj.roundRect(290, 45, 285, 200, 4, stroke=1, fill=0)

    def generate_report(self):
        """This function is responsible in generating a 
        PDF report and saving it to a chosen folder."""
        sum = StatsRetriever(self.config)
        steam = StatsRetriever(self.config, (1,))
        gog = StatsRetriever(self.config, (2,))
        epic = StatsRetriever(self.config, (3,))
        pdfmetrics.registerFont(TTFont('jersey_15', 'Jersey15-Regular.ttf'))
        c = canvas.Canvas(
            f'{self.config["STORAGE_FOLDER"]}/Weekly_Report.pdf', pagesize=letter)
        c.setFont('jersey_15', 30)
        c.setFillColorRGB(0.6, 0.09, 10.8)
        text_width = pdfmetrics.stringWidth(
            'GameScraper Weekly Report', 'jersey_15', 30)
        c.drawString((self.page_width-text_width) /
                     2.0, 750, 'GameScraper Weekly Report')
        c.drawImage('game_scraper_logo.png',
                    x=470, y=735, width=50, height=50)
        c.setFont('jersey_15', 20)
        c.drawString(50, 695, 'Summary')
        c.setFillColorRGB(0.6, 0.50, 30.0)
        c.drawString(50, 715, f'Date: {str(datetime.now().date())}')
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


def handler(event: dict = None, context: dict = None) -> dict:
    """
    Handler function for generating & sending emails.
    """
    report_maker_obj = ReportMaker(os.environ)
    report_maker_obj.generate_report()
    emailer_obj = Alerter(os.environ)
    subscribers = emailer_obj.get_subscription_emails()
    emailer_obj.send_email(subscribers)

    return {"message": "Emails sent"}


if __name__ == "__main__":
    load_dotenv()
    report_maker_obj = ReportMaker(os.environ)
    report_maker_obj.generate_report()
    emailer_obj = Alerter(os.environ)
    subscribers = emailer_obj.get_subscription_emails()
    emailer_obj.send_email(subscribers)
