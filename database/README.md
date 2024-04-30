## Description

> This Folder is responsible for defining and creating the tables in our database.


## Requirements
There are no requirements for this folder.

## Environment Variables
In order to run the scripts you will need the following environment variables:

- DB_PASSWORD
- DB_NAME
- DB_USER
- DB_HOST
- DB_PORT

## The Scripts
This folder contains the following scripts:

- **schema.sql**  
This script drops the tables that may be in the database already, then redefines the tables, and seeds them with some static data.  
  
- **run_script.sh**  
This script is used to run **schema.sql**.  
  
  Run from the command line using: 
  >bash run_script.sh
  
- **connect.sh**  
This script is used to connect to the database.  
  
  Run from the command line using:
  >bash connect.sh

## ERD Diagram

This diagram demonstrates the database structure and the connections between the tables.

![ERD Diagram](<../diagrams/ERD diagram.png>)