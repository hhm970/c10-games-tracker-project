## Description

This folder is responsible for the extraction phase of our pipeline, it contains three separate folders, one for each of the websites were are collecting data from.

### The Why
This folder is important because it contains the files that collect the data from each of our three sources Steam, Epic and Good Old Games (GOG). We decided to split this folder into three sub-folders, because we thought this made it completely clear which scripts relate to which websites. It also allows us to tailor each extract script specifically to the needs of each website that we are extracting from.

## Requirements
The requirements for each folder are defined in their respective _requirements.txt_.


## Environment Variables
In order to run the scripts you will need the following environment variables, in a *.env* file:


- ```GOG_BASE_URL```
- ```EPIC_BASE_URL```
- ```STEAM_BASE_URL```


## The Scripts
Each folder contains the following scripts:

- **extract_X.py**  
This script extracts data from the website.  

   Run from the command line using: 
  >```python3 extract_X.py```
  
- **Dockerfile**  
This script is used to dockerise the extract file.  
  
  Run from the command line using: 
  >```docker build -t extract .```  
  >```docker run --env-file .env extract```  


- **test_extract_X.py**  
This script tests **extract_X.py**.  

   Run from the command line using: 
  >```pytest test_extract_X.py```


- **conftest.py**  
This script defines variables used within the testing files.  