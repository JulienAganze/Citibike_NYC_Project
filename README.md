# NYC Bike project

## Objective



## Architecture


## Problem statement




## Main objective

The following steps were performed to analyze the air quality data for the 100 Polish cities:



## Dataset description






## Proposal

### Technologies
## What technologies are being used?
- Cloud: [Google Cloud](https://cloud.google.com)
- Infrastructure: [Terraform](https://www.terraform.io/)
- Orchestration: [Prefect](https://www.prefect.io/)
- Data lake: [Google Cloud Storage](https://cloud.google.com/storage)
- Data transformation: [DBT](https://www.getdbt.com/)
- Data warehouse: [BigQuery](https://cloud.google.com/bigquery)
- Data visualization: [Google Looker Studio](https://cloud.google.com/looker)


### Repository organization
- \dbt: dbt files (dbt_project.yml, models, etc.).
- \airflow: prefect flows files (etl_tasks.py, history_parameterized_flow.py, current_parameterized_flow.py, docker_deployment.py).  
#- \images: pictures.  
- \terraform: terraform files for the definition of the infrastructure to deploy.  
- \README.md: this document.  
- \setup_gcp.md: instructions to configure cgp account.  
  

**Infrastructure as code:**  

Use Terraform to create a bucket GCS and dataset in BQ  

  **Orchestration:**  


**Transformations using dbt:**  
  
 

  
  Connect Google Data Studio to BQ dataset and design dashboard  

  ## Results

**Dashboard**


## Setup and running



### Setup




### Run pipelines
1. Setup your Google Cloud environment
- Create a [Google Cloud Platform project](https://console.cloud.google.com/cloud-resource-manager)
- Configure Identity and Access Management (IAM) for the service account, giving it the following privileges: BigQuery Admin, Storage Admin and Storage Object Admin
- Download the JSON credentials and save it, e.g. to `~/.gc/<credentials>`
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- Let the [environment variable point to your GCP key](https://cloud.google.com/docs/authentication/application-default-credentials#GAC), authenticate it and refresh the session token
```bash
export GOOGLE_APPLICATION_CREDENTIALS=<path_to_your_credentials>.json
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default login
```
2. Install all required dependencies into your environment
```bash
pip install -r requirements.txt
```
3. Terraform
`cd terraform`
`terraform init`
`terraform plan -var="project=<your-gcp-project-id>"`
`terraform apply -var="project=<your-gcp-project-id>"`


5. Setup your orchestration


```
