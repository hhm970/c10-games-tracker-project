## Description

This folder is responsible for creating the dashboard that displays metrics and graphs about our data.  

### The Why
The dashboard is important for business users to see graphs and metrics about the latest releases, this will allow them to identify trends in the market and tailor their games or marketing campaigns to suit these trends.


## Requirements
The requirements for this folder are:
- ```streamlit```
- ```pandas```
- ```altair```
- ```boto3```
- ```python-dotenv```
- ```psycopg2-binary```



## Environment Variables
In order to run the scripts you will need the following environment variables, in a *.env* file:


- ```AWS_KEY```
- ```AWS_SECRET```
- ```AWS_REGION```
- ```DB_PASSWORD```
- ```DB_NAME```
- ```DB_USER```
- ```DB_HOST```
- ```DB_PORT```


## The Scripts
The folder contains the following scripts:

- **Home.py**  
This script defines the code for the homepage of the dashboard, and is where the dashboard should be run from.  

   Run from the command line using: 
  >```streamlit run Home.py```
  
- **Dockerfile**  
This script is used to dockerise the dashboard.  
  
  Run from the command line using: 
  >```docker build -t dashboard .```   
  >```Docker run --env-file .env  -p 8501:8501 dashboard```


- **build-dashboard.sh**  
This script is used to build the dashboard.  
  
  Run from the command line using: 
  >```bash build-dashboard.sh```
  
- **run-dashboard.sh**  
This script is used to run the database.  
  
  Run from the command line using:
  >```bash run-dashboard.sh```



### The Folders
The dashboard folder contains the following folders:

- **.streamlit**  
This folder defines the style and colours (configuration) of the dashboard.  


  
- **pages**  
This folder defines the different pages of the dashboard.