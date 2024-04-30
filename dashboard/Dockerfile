FROM python:latest
WORKDIR ./app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir pages
RUN mkdir .streamlit

COPY Home.py .
COPY pages/Epic.py pages
COPY pages/GOG.py pages
COPY pages/Steam.py pages
COPY pages/Daily_Notifications.py pages
COPY pages/Weekly_Newsletter.py pages
COPY .streamlit/config.toml .streamlit
ENTRYPOINT ["streamlit","run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]