## Description

This Folder is responsible for loading data into in our database.

### The Why
This folder is important because it bridges the gap between collecting the data with our extraction files and our database. It takes the data, cleans it and then loads it into our database.  


## Requirements
The requirements for this folder are:
- ```psycopg2-binary```
- ```pytest```
- ```pytest-cov```
- ```pylint```


## Environment Variables
In order to run the scripts you will need the following environment variables, in a *.env* file:


- ```DB_PASSWORD```
- ```DB_NAME```
- ```DB_USER```
- ```DB_HOST```
- ```DB_PORT```


## The Scripts
This folder contains the following scripts:

- **load.py**  
This script uploads data to our database.  

   Run from the command line using: 
  >```python3 load.py```
  
- **Dockerfile**  
This script is used to dockerise **load.py**.  
  
  Run from the command line using: 
  >```docker build -t load .```  
  >```docker run --env-file .env load```  


- **test_load.py**  
This script tests **load.py**.  

   Run from the command line using: 
  >```pytest test_load.py```


- **conftest.py**  
This script defines variables used within **test_load.py**.  

