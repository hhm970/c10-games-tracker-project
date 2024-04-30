## Description

This Folder is responsible for defining and creating the tables in our database.


## Requirements
The requirements for this folder are:
- python-dotenv
- boto3
- pylint


## Environment Variables
In order to run the scripts you will need the following environment variables, in a *.env* file:

- AWS_KEY
- AWS_SECRET


## The Scripts
This folder contains the following scripts:

- **alert.py**  
This script sends SNS alerts to subscribers of topics, based on newly released games.  

   Run from the command line using: 
  >python3 alert.py
  
- **Dockerfile**  
This script is used to dockerise **alert.py**.  
  
  Run from the command line using: 
  >docker build -t alert .  
  >docker run --env-file .env alert  
