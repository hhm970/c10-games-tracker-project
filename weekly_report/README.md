## Description

This Folder is responsible for sending weekly reports via email to our users/subscribers.


## Requirements
The requirements for this folder are:
- pylint
- psycopg2-binary
- reportlab
- altair
- pandas
- vl-convert-python
- boto3
- wordcloud
- python-dotenv


## Environment Variables
In order to run the scripts you will need the following environment variables, in a *.env* file:

- DB_PASSWORD
- DB_NAME
- DB_USER
- DB_HOST
- DB_PORT
- ACCESS_KEY_ID (AWS)
- SECRET_ACCESS_KEY (AWS)
- STORAGE_FOLDER


## The Scripts
This folder contains the following scripts:

- **generate_report.py**  
This script generates a pdf report of the week (summarised & individual) based on data from the database and emails this report to subscribers every monday morning.

   Run from the command line using: 
  >python3 generate_report.py
  
- **Dockerfile**  
This script is used to dockerise **generate_report.py**.  
  
  Run from the command line using: 
  >docker build -t generate_report .  
  >docker run --env-file .env generate_report  
