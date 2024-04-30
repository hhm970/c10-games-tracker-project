## Description

This Folder contains all the terraform files to create all our AWS services.


## Requirements
There are no requirements for this folder.

## Environment Variables
In order to run the scripts you will need the following environment variables in a *terraform.tfvars* file:

- DB_PASSWORD
- DB_NAME
- DB_USER
- DB_HOST
- DB_PORT
- GOG_BASE_URL
- EPIC_BASE_URL
- STEAM_BASE_URL
- AWS_KEY
- AWS_SECRET

## The Scripts
This folder contains the following scripts:

- **database.tf**  
This script creates an RDS database.  
  - **dashboard.tf**
  This script creates an ECS Service which continually deploys the dashboard.
  
- **pipeline_eventbridge.tf**  
This script creates an EventBridge Schedule which triggers every evening at 23:50, and targets the StepFunction that executes the pipeline.  
  
- **pipeline_lambdas.tf**  
This script creates all the Lambda functions which are used in the pipeline StepFunction. 

- **pipeline_stepfunction.tf**  
This script creates a StepFunction that executes the pipeline.  
  
- **provider.tf**  
This script defines the provider.  
  
- **report_eventbridge.tf**  
This script creates an EventBridge Schedule which triggers every Monday at 09:00am, and targets the StepFunction that sends out the weekly report.  
  
- **report_lamda.tf**  
This script creates the Lambda functions which are used in the weekly report StepFunction.  
  
- **report_stepfunction.tf**  
This script creates a StepFunction that sends the weekly reports.    

- **variables.tf**  
This script defines the types for all the secret variables.  
  
  
To create all the AWS services defined here, in the command line run:
> terraform apply

To destroy the terraformed AWS services defined here, in the command line run:
> terraform destroy