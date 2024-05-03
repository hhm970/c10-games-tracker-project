FROM python:latest
RUN mkdir /gen_report
RUN mkdir /gen_report/diagrams
WORKDIR /gen_report 
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY game_scraper_logo.png .
COPY Jersey15-Regular.ttf .
COPY generate_report.py .
CMD [ "python3","generate_report.py"]