## Description

> This Project is responsible for helping users to keep up with the latest releases as well as understand latest gaming trends.

New PC games are released every day on different platforms; it’s hard to keep up with new releases, and it’s even harder to understand the trends in gaming. We aim to create a data pipeline that tracks new new releases on major PC platforms.  


## Stakeholder Requirements
- `Gamers` - know what the latest game releases are.
- `Developers`- understand the market more effectively.

### Deliverables


### Dashboard Requirements

The requirements are:


## Requirements

### Pre-requisites

- Python 3.11
- pip3
- AWS CLI
- Docker
- Terraform

### Imports

 ```sh
   pip3 install -r requirements.txt
   ```

**Secrets/Authentication**
> [!IMPORTANT]  
> To be able to run these scripts locally the following details must be provided in the `.env` file.



## Deployment

- Run the following command to deploy the project:
  ```sh
  cd terraform
  terraform init
  terraform apply
  ```

## Files and Folder Structure Explained

- root folder: Contains the following files:

- .github folder: Contains code related to the github actions.
- dashboard folder: Contains code related to the dashboard.

- pipeline folder: Contains code and resources related to the pipeline.

- terraform folder: Contains code and resources related to the terraform.


## ERD
![ERD Diagram](<diagrams/ERD diagram.png>)

## Architecture Diagram
![Architecture Diagram](<diagrams/game-tracker.drawio.png>)
[Architecture Drawio](https://drive.google.com/file/d/1eyiUtG28TyXLwHTw9276TIMAXI4Pgwh3/view?usp=sharing)



## Maintainers

* [hhm970](https://github.com/hhm970)
* [annalisev](https://github.com/annalisev)
* [EIbironke](https://github.com/EIbironke)
* [shindym](https://github.com/shindym)

