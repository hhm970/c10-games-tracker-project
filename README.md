# Games Tracker Project 👾
## Description
**This Project is responsible for helping users to keep up with the latest game releases as well as understand the latest gaming trends.**

>New PC games are released every day on different platforms; it’s hard to keep up with new releases, and it’s even harder to understand the trends in gaming. We aim to create a data pipeline that tracks new new releases on major PC platforms. We will also produce a dashboard with key metrics and graphs for comparisons between different websites. Furthermore we will also send email notifications to our subscribers- weekly PDF reports and daily notifications about new releases that day.   

## Data Sources
- `Epic Games` - GraphQL API
- `GOG` - Webscraping
- `Steam` - Webscraping

## Users
- `Gamers` - Know what the latest game releases are.

- `Developers`- Understand the market more effectively and produce games which align with current market trends.

- `Retailers` - Understand latest market trends - use knowledge to know what games to push/recommend to users.

## Requirements

### Pre-requisites

- ```Python 3.11```
- `pip3`
- `awscli`
- `Docker`
- `Terraform`
- `PostgreSQL`

### Imports
Each sub-folder in this repository holds their own `requirements.txt` file. This is has been done to ensure clarity in what modules the scripts require.

In each folder's directory to download the requirements use this command:

```sh
pip3 install -r requirements.txt
  ```

**Secrets/Authentication**
> [!IMPORTANT]  
> To be able to run these scripts locally the details must be provided in a `.env` file within each folder.
> Further details of the secrets required can be found in sub-folders `README.md`


## Cloud Deployment
This project has been designed to be able to hosted on the cloud. 


Run the following command to deploy the project:

```sh
  cd terraform
  terraform init
  terraform apply
  ```

> [!NOTE]  
> The ECR repositories were made via the AWS console. In order to be able to run the terraform script you must create the following ECR repositories listed below before.

#### ECR Repositories
- c10-games-dashboard
- c10-games-db-load
- c10-games-epic-extract
- c10-games-gog-scrape
- c10-games-steam-scrape
- c10-games-weekly-report

## Folder Structure Explained

root: Contains the following files:

- `.github`: Contains code related to the github actions.

- `dashboard`: Contains code related to the dashboard.

- `pipeline`: Contains code and resources related to the pipeline and notification generation.

- `terraform`: Contains code and resources related to terraforming cloud infrastructure.

- `database`: contains code and resources related to the RDS database.

- `diagrams`: Contains images related to this project.

- `weekly_report`: contains code and resources related to the report generation and distribution.


> [!NOTE]  
> Our storage system for the emails inputted when subscribing to weekly newsletters is not secure. Please do not actually input your email here.


## ERD
![ERD Diagram](<diagrams/ERD diagram.png>)

## Architecture Diagram
![Architecture Diagram](<diagrams/games-tracker.drawio.png>)
[Architecture Drawio](https://drive.google.com/file/d/1eyiUtG28TyXLwHTw9276TIMAXI4Pgwh3/view?usp=sharing)



## Maintainers
### The GameScraper Team 🚀
* [hhm970](https://github.com/hhm970)
* [annalisev](https://github.com/annalisev)
* [EIbironke](https://github.com/EIbironke)
* [shindym](https://github.com/shindym)

